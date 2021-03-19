from z3 import Solver, ExprRef, sat, Not
from symex.Environment import Environment
from symex.expression import evalExpression
import symex.evaluation as e
import copy
from typing import Dict


def evalIf(ast: Dict, s: Solver, env: Environment) -> ExprRef:
    c: ExprRef = evalExpression(ast["cond"], s, env)
    if satisfiable(c):
        e.phpEvalAst(ast["stmts"], s, Environment(env))
    if satisfiable(Not(c)):
        e.phpEvalAst(ast["elseifs"], s, Environment(env))
        if ast["else"] is not None:
            elseSolver: Solver = copy.deepcopy(s)
            elseSolver.add(Not(c))
            for eif in ast["elseifs"]:
                elseSolver.add(Not(evalExpression(eif["cond"], s, env)))
            if elseSolver.check() == sat:
                e.phpEval(ast["else"], s, Environment(env))


def evalElseIf(ast: Dict, s: Solver, env: Environment):
    if satisfiable(evalExpression(ast["cond"], s, env)):
        e.phpEvalAst(ast["stmts"], s, env)


def evalElse(ast: Dict, s: Solver, env: Environment):
    e.phpEvalAst(ast["stmts"], s, env)


def satisfiable(exp: ExprRef):
    s = Solver()
    s.add(exp)
    return s.check() == sat
