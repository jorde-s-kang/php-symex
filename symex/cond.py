from z3 import Solver, ExprRef, sat, Not
from symex.Environment import Environment
from symex.expression import evalExpression
import symex.evaluation as e
import copy
from typing import Dict


def evalIf(ast: Dict, env: Environment) -> ExprRef:
    c: ExprRef = evalExpression(ast["cond"], env)
    if satisfiable(c):
        nenv = env.fork()
        nenv.symenv.constraints.add(c)
        e.phpEvalAst(ast["stmts"], env.fork())
    e.phpEvalAst(ast["elseifs"], env)
    if ast["else"] is not None:
        nenv = env.fork()
        elseSolver = nenv.symenv.constraints
        elseSolver.add(Not(c))
        for eif in ast["elseifs"]:
            elseSolver.add(Not(evalExpression(eif["cond"], env)))
        if elseSolver.check() == sat:
            e.phpEval(ast["else"], nenv)


def evalElseIf(ast: Dict, env: Environment):
    c = evalExpression(ast["cond"], env)
    if satisfiable(c):
        nenv = env.fork()
        nenv.symenv.constraints.add(c)
        e.phpEvalAst(ast["stmts"], env)


def evalElse(ast: Dict, env: Environment):
    print(env.symenv.constraints)
    e.phpEvalAst(ast["stmts"], env)


def satisfiable(exp: ExprRef):
    s = Solver()
    s.add(exp)
    return s.check() == sat
