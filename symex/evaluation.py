from z3 import ExprRef
from .Environment import Environment
from pampy import match
import phpparser as p
from z3 import Solver
from typing import List, Dict

from symex.UnknownVal import UnknownVal
import symex.expression as expr
import symex.cond as cond
import symex.loop as loop
import symex.func as func
import symex.obj as obj

def phpEvalInline(data: str, getVars: Dict = {}, postVars: Dict = {}, constraints = []) -> Environment:
    """
    Evaluates a given inline PHP statement
    Args:
        data: A PHP string beginning '<?php'
        getVars: Bind _GET superglobal variables.
        postVars: Bind _POST superglobal variables.
        constraints: A list of constraints on symbolic values in getVars and postVars

    Returns:
        Environment: The resulting state of the program
    """
    env = Environment()
    env.define("_GET", getVars)
    env.define("_POST", postVars)    
    for c in constraints:
        env.symenv.constraints.append(c)
    ast = p.parseInline(data)
    return phpEvalAst(ast, env)


def phpEvalFile(fname: str, getVars: Dict = {}, postVars: Dict = {}, constraints = []):
    """
    Evaluates a given PHP file
    Args:
        fname: The name of the file
        getVars: Bind _GET superglobal variables.
        postVars: Bind _POST superglobal variables.
        constraints: A list of constraints on symbolic values in getVars and postVars

    Returns:
        Environment: The resulting state of the program
    """
    env: Environment = Environment()
    env.define("_GET", getVars)
    env.define("_POST", postVars)
    ast: List = p.parseFile(fname)
    return phpEvalAst(ast, env)


def phpEvalAst(ast: List[Dict], env: Environment):
    """
    Evaluates the output of Phpparser.parse()
    Args:
        ast: A JSON formatted Abstract Syntax Tree
        env: A state of a program
    Returns:
        The resulting state of the program
    """
    for stmt in ast:
        phpEval(stmt, env)
    return env


def phpEval(ast: Dict, env: Environment) -> ExprRef:
    """
    Evaluates a JSON AST node
    Args:
        ast: A JSON formatted Abstract Syntax Tree
        env: A state of a program
    Returns:
         The result of the node
    """
    line = ast["attributes"]["startLine"]
    print(f"Running {ast['nodeType']} at line {line}.")
    fn = match(ast,
               {'nodeType': 'Stmt_Expression'}, lambda x: expr.evalExpression,
               {'nodeType': 'Stmt_Echo'},       lambda x: phpEvalEcho,
               {'nodeType': 'Stmt_If'},         lambda x: cond.evalIf,
               {'nodeType': 'Stmt_ElseIf'},     lambda x: cond.evalElseIf,
               {'nodeType': 'Stmt_Else'},       lambda x: cond.evalElse,
               {'nodeType': 'Stmt_While'},      lambda x: loop.evalWhile,
               {'nodeType': 'Stmt_For'},        lambda x: loop.evalFor,
               {'nodeType': 'Stmt_Foreach'},    lambda x: loop.evalForEach,
               {'nodeType': 'Stmt_Function'},   lambda x: func.define,
               {'nodeType': 'Stmt_Class'},      lambda x: obj.genClass,
               {'nodeType': 'Stmt_Nop'},        lambda x: lambda x,y: None,
               {'nodeType': 'Stmt_InlineHTML'}, lambda x: lambda x,y: None)
    return fn(ast, env)


def phpEvalEcho(ast: Dict, env: Environment):
    """
    Evaluates a list of expressions and prints them to the screen.
    Args:
        ast: A JSON formatted Abstract Syntax Tree
        env: A state of a program
    """
    exprs = [expr.evalExpression(ast, env) for ast in ast["exprs"]]
    print(*exprs)
