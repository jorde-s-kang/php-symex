from z3 import Solver, ExprRef, BoolRef
from symex.Environment import Environment
from typing import Callable, List, Tuple, Dict
import symex.lookup as lookup
import re
from pampy import match, _
from symex.Exceptions import ExpressionError
import symex.datatypes as dt
import symex.func as func
def evalExpression(exp: Dict, env: Environment):
    """
    Evaluates a PHP expression
    :param exp: The abstract syntax tree of an expression
    :param env: The environment the expression will be called in
    """

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
               "Expr_PropertyFetch",            lambda x: propertyFetch,
               "Expr_Include",                  lambda x: lambda x,y: None)
    return fn(e, env)


def funcCall(ast: Dict, env: Environment):
    """
    Calls a defined function
    :param ast: The abstract syntax tree of a function call
    :param env: The environment the expression will be called in
    """
    args: List = [evalExpression(arg["value"], env) for arg in ast["args"]]
    fn = lambda x, y: None
    try:
        fn = func.phpFunctions[ast["name"]["parts"][0]]
    except KeyError:
        pass
    if callable(fn):
        return fn(*args, env=env)
    else:
        return fn.run(args, env)

def binop(ast: Dict, env: Environment) -> Callable:
    """
    Evaluates a binary operator expression
    :param ast: The abstract syntax tree of a binary operation
    :param env: The environment the expression will be called in
    """
    op: Callable = lookup.get_binop(ast["nodeType"])
    def binaryOperator(ast: Dict, env: Environment):
        left  = evalExpression(ast["left"], env)
        right = evalExpression(ast["right"], env)
        return op(left, right)
    return binaryOperator(ast, env)


def parseValue(ast: Dict, env: Environment):
    """
    Parses a scalar value
    :param ast: The abstract syntax tree of a scalar value
    :param env: The environment the expression will be called in
    """
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
    """For some reason booleans are treated as constants rather than a
    typical datatype. This is just to handle booleans.
    :param ast: The abstract syntax tree of a scalar value
    :param env: The environment the expression will be called in
    """
    consts = {"True": True,
              "False": False}
    return consts[ast["name"]["parts"][0]]

def varAssign(ast: Dict, env: Environment):
    """Define a variable in the current environment
    :param ast: The abstract syntax tree of a variable assignment
    :param env: The environment the expression will be called in
    """
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
    """Lookup the variable in the current environment.
    :param ast: The abstract syntax tree of a variable lookup
    :param env: The environment the expression will be called in
    """
    var = ast["name"]
    val = env.lookup(var)
    return val

def array(ast: Dict, env: Environment):
    """ Evaluate a PHP array
    :param ast: The abstract syntax tree of an array
    :param env: The environment the expression will be called in
    """
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
    """Fetches an item from an array
    :param ast: The abstract syntax tree of an array lookup
    :param env: The environment the expression will be called in
    """
    arr = evalExpression(ast["var"], env)
    ind = evalExpression(ast["dim"], env)
    return arr[ind]

def encapsedString(ast, env):
    """
    Translates an encapsulated string in PHP into a python array
    :param ast: The abstract syntax tree of an encapsulated string
    :param env: The environment the expression will be called in
    """
    return [evalExpression(p, env) for p in ast]

def methodCall(ast, env):
    """
    Calls a method on an object in PHP
    :param ast: The abstract syntax tree of a method call
    :param env: The environment the expression will be called in
    """
    v = evalExpression(ast["var"], env)
    method = getattr(v, ast["name"]["name"])
    args: List = [evalExpression(arg["value"], env) for arg in ast["args"]]
    return method(args, env=env)

def propertyFetch(ast, env):
    """
    Fetches a property from an object in PHP
    :param ast: The abstract syntax tree of a property fetch
    :param env: The environment the expression will be called in
    """
    obj = evalExpression(ast["var"], env)
    return getattr(obj, ast["name"]["name"])
