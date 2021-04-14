from z3 import ExprRef
from .Environment import Environment
from pampy import match
import phpparser as p
from z3 import Solver
from typing import List, Dict

import symex.expression as expr
import symex.cond as cond
import symex.loop as loop
import symex.func as func
import symex.obj as obj

def phpEvalInline(data: str, getVars: Dict = {}, postVars: Dict = {}, constraints = []) -> Environment:
    """
    Evaluates a given inline PHP statement
    :param data: A PHP string beginning '<?php'
    :param getVars: Bind _GET superglobal variables.
    :param postVars: Bind _POST superglobal variables.
    :param constraints: A list of constraints on symbolic values in getVars and postVars

    :returns: The resulting state of the program
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
    Parameters:
    fname: The name of the file
    :param getVars: Bind _GET superglobal variables.
    :param postVars: Bind _POST superglobal variables.
    :param constraints: A list of constraints on symbolic values in getVars and postVars

    :returns: The resulting state of the program
    """
    env: Environment = Environment()
    env.define("_GET", getVars)
    env.define("_POST", postVars)
    ast: List = p.parse_file(fname)
    return phpEvalAst(ast, env)


def phpEvalAst(ast: List[Dict], env: Environment):
    """
    Evaluates the output of Phpparser.parse()
    :param ast: A JSON formatted Abstract Syntax Tree
    :param env: A state of a program

    :returns: The resulting state of the program
    """
    for stmt in ast:
        phpEval(stmt, env)
    return env


def phpEval(ast: Dict, env: Environment) -> ExprRef:
    """
    :param ast: A JSON formatted Abstract Syntax Tree
    :param env: A state of a program

    :returns: The resulting state of the program
    """
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
    """
    exprs = [expr.evalExpression(ast, env) for ast in ast["exprs"]]
    print(*exprs)
