from z3 import Solver, ExprRef, BoolRef
from symex.Environment import Environment
from typing import Callable, List, Tuple, Dict
import symex.lookup as lookup
import re
from pampy import match, _
from symex.Exceptions import ExpressionError
import symex.datatypes as dt
import symex.func as func
def evalExpression(exp: Dict, env: Environment) -> ExprRef:
    e = None
    try:
        if exp["nodeType"] != "Expr_Assign":
            e = exp["expr"]
        else:
            raise KeyError()
    except KeyError:
        e = exp
    except TypeError:
        return None
    # print(e)
    fn = match(e["nodeType"],
               re.compile("^Expr_BinaryOp_.*"), lambda x: binop,
               re.compile("^Scalar_.*"),        lambda x: parseValue,
               "Expr_FuncCall",                 lambda x: funcCall,
               "Expr_Assign",                   lambda x: varAssign,
               "Expr_Variable",                 lambda x: varLookup,
               "Expr_Array",                    lambda x: array,
               "Expr_ArrayDimFetch",            lambda x: arrayFetch,
               "Expr_ConstFetch",               lambda x: constFetch,
               "Expr_MethodCall",               lambda x: methodCall,
               None,                            lambda x: lambda x, y: None,
               "Expr_PropertyFetch",            lambda x: propertyFetch)
    return fn(e, env)


def funcCall(ast: Dict, env: Environment):
    print(func.phpFunctions)
    args: List = [evalExpression(arg["value"], env) for arg in ast["args"]]
    fn = lambda x, y: None
    try:
        fn = func.phpFunctions[ast["name"]["parts"][0]]
    except KeyError:
        pass
    print(fn)
    if callable(fn):
        return fn(*args, env=env)
    else:
        return fn.run(args, env)

def binop(ast: Dict, env: Environment) -> Callable:
    op: Callable = lookup.get_binop(ast["nodeType"])
    def binaryOperator(ast: Dict, env: Environment):
        left  = evalExpression(ast["left"], env)
        right = evalExpression(ast["right"], env)
        return op(left, right)
    return binaryOperator(ast, env)


def parseValue(ast: Dict, env: Environment):
    t = match(ast["nodeType"],
              "Scalar_LNumber",  lambda x: lambda v, env: int(v),
              "Boolean",         lambda x: lambda v, env: bool(v),
              "Scalar_String",   lambda x: lambda v, env: str(v),
              "Scalar_DNumber",  lambda x: lambda v, env: float(v),
              "Scalar_Encapsed", lambda x: lambda v, env: encapsedString(v, env),
              "Scalar_EncapsedStringPart", lambda x: lambda v, env: str(v))
    try:
        return t(ast["value"], env)
    except KeyError:
        return t(ast["parts"], env)

def constFetch(ast: Dict, env: Environment):
    consts = {"True": True,
              "False": False}
    return consts[ast["name"]["parts"][0]]

def varAssign(ast: Dict, env: Environment):
    propfetch = False
    propfetch = ast["var"]["nodeType"] == "Expr_PropertyFetch"
    if propfetch:
        obj = ast["var"]
        var = evalExpression(obj["var"], env)
        identifier = obj["name"]["name"]
        setattr(var, identifier, evalExpression(ast["expr"], env)) 
    else:
        var = None
        val = evalExpression(ast["expr"], env)
        if ast["var"]["nodeType"] == "Expr_Variable":
            var = ast["var"]["name"]
        if type(val).__bases__[0] == ExprRef:
            env.define(var, val)
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

def encapsedString(ast, env):
    return [evalExpression(p, env) for p in ast]

def methodCall(ast, env):
    v = evalExpression(ast["var"], env)
    method = getattr(v, ast["name"]["name"])
    args: List = [evalExpression(arg["value"], env) for arg in ast["args"]]
    return method(args, env=env)

def propertyFetch(ast, env):
    obj = evalExpression(ast["var"], env)
    return getattr(obj, ast["name"]["name"])
