from z3 import ExprRef
from .Environment import Environment
from pampy import match
from phpparser import Parser
from z3 import Solver
from typing import List, Dict

import symex.expression as expr
import symex.cond as cond
import symex.loop as loop
import symex.func as func

def phpEvalInline(data: str, getVars: Dict = {}, postVars: Dict = {}, constraints = []):
    """
    Evaluates a given inline PHP statement
    Parameters:
    data: A PHP string beginning '<?php'
    """
    p = Parser()
    env = Environment()
    env.define("_GET", getVars)
    env.define("_POST", postVars)    
    for c in constraints:
        env.symenv.constraints.append(c)
    print(constraints)
    ast = p.parse_inline(data)
    return phpEvalAst(ast, env)


def phpEvalFile(fname: str, getVars: Dict = {}, postVars: Dict = {}, constraints = []):
    """
    Evaluates a given PHP file
    Parameters:
    fname: The name of the file 
    """
    p: Parser = Parser()
    env: Environment = Environment()
    env.define("_GET", getVars)
    env.define("_POST", postVars)
    ast: List = p.parse_file(fname)
    return phpEvalAst(ast, env)


def phpEvalAst(ast: List[Dict], env: Environment):
    """
    Evaluates the output of Phpparser.parse()
    """
    for stmt in ast:
        phpEval(stmt, env)
    return env


def phpEval(ast: Dict, env: Environment) -> ExprRef:
    fn = match(ast,
               {'nodeType': 'Stmt_Expression'}, lambda x: expr.evalExpression,
               {'nodeType': 'Stmt_Echo'},       lambda x: phpEvalEcho,
               {'nodeType': 'Stmt_If'},         lambda x: cond.evalIf,
               {'nodeType': 'Stmt_ElseIf'},     lambda x: cond.evalElseIf,
               {'nodeType': 'Stmt_Else'},       lambda x: cond.evalElse,
               {'nodeType': 'Stmt_While'},      lambda x: loop.evalWhile,
               {'nodeType': 'Stmt_For'},        lambda x: loop.evalFor,
               {'nodeType': 'Stmt_Foreach'},    lambda x: loop.evalForEach,
               {'nodeType': 'Stmt_Function'},   lambda x: func.define)
    return fn(ast, env)


def phpEvalEcho(ast: Dict, env: Environment):
    exprs = [expr.evalExpression(ast, env) for ast in ast["exprs"]]
    print(*exprs)
