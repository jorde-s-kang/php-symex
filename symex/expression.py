from z3 import Solver, ExprRef, BoolRef
from symex.Environment import Environment
from typing import Callable, List, Tuple, Dict
import symex.lookup as lookup
import re
from pampy import match, _
from symex.Exceptions import ExpressionError
import symex.datatypes as dt

def evalExpression(exp: Dict, env: Environment) -> ExprRef:
    e = None
    try:
        if exp["nodeType"] != "Expr_Assign":
            e = exp["expr"]
        else:
            raise KeyError()
    except KeyError:
        e = exp
    # print(e)
    fn = match(e["nodeType"],
               re.compile("^Expr_BinaryOp_.*"), lambda x: binop,
               re.compile("^Scalar_.*"),        lambda x: parseValue,
               "Expr_FuncCall",                 lambda x: funcCall,
               "Expr_Assign",                   lambda x: varAssign,
               "Expr_Variable",                 lambda x: varLookup,
               "Expr_Array",                    lambda x: array,
               "Expr_ArrayDimFetch",            lambda x: arrayFetch,
               "Expr_ConstFetch",               lambda x: constFetch
    )
    return fn(e, env)


def funcCall(ast: Dict, env: Environment):
    args: List = [evalExpression(arg["value"], env) for arg in ast["args"]]
    fn: Callable = lookup.get_fn(ast["name"]["parts"][0])
    return fn(*args)


def binop(ast: Dict, env: Environment) -> Callable:
    op: Callable = lookup.get_binop(ast["nodeType"])
    def binaryOperator(ast: Dict, env: Environment):
        left  = evalExpression(ast["left"], env)
        right = evalExpression(ast["right"], env)
        return op(left, right)
    return binaryOperator(ast, env)


def parseValue(ast: Dict, env: Environment):
    t = match(ast["nodeType"],
              "Scalar_LNumber", lambda x: int,
              "Boolean", lambda x: bool,
              "Scalar_String", lambda x: str,
              "Scalar_DNumber", lambda x: float)
    return t(ast["value"])

def constFetch(ast: Dict, env: Environment):
    consts = {"True": True,
              "False": False}
    return consts[ast["name"]["parts"][0]]

def varAssign(ast: Dict, env: Environment):
    var = None
    val = evalExpression(ast["expr"], env)
    if ast["var"]["nodeType"] == "Expr_Variable":
        var = ast["var"]["name"]
    if type(val).__bases__[0] == ExprRef:
        env.symenv.define(var, val)
    else:
        env.define(var, val)

def varLookup(ast: Dict, env: Environment):
    var = ast["name"]
    val = env.lookup(var)
    return val

def array(ast: Dict, env: Environment):
    items = dict()
    c = 0
    for i in ast["items"]:
        val = evalExpression(i["value"], env)
        if i["key"] is not None:
            items[evalExpression(i["key"], env)] = val
        else:
            items[c] = val
            c += 1
    return items

def arrayFetch(ast: Dict, env: Environment):
    arr = evalExpression(ast["var"], env)
    ind = evalExpression(ast["dim"], env)
    return arr[ind]