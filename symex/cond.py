from z3 import Solver, ExprRef, sat, Not
from symex.Environment import Environment
from symex.expression import evalExpression
import symex.evaluation as e
import copy
from typing import Dict


def evalIf(ast: Dict, env: Environment) -> ExprRef:
    c: ExprRef = evalExpression(ast["cond"], env)
    print(f"INITIAL CONSTRAINTS: {env.symenv.constraints}")
    nenv = env.fork()
    nenv.symenv.constraints.append(c)
    if nenv.symenv.sat():
        nenv = env.fork()
        nenv.symenv.constraints.append(c)
        print(f"TAKING IF PATH: {nenv.symenv.constraints}")
        e.phpEvalAst(ast["stmts"], nenv)
    e.phpEvalAst(ast["elseifs"], nenv)
    if ast["else"] is not None:
        print("else fork")
        nenv = env.fork()
        print(f"FORKED ELSE CONSTRAINTS: {nenv.symenv.constraints}")
        nenv.symenv.constraints.append(Not(c))
        print(f"ADDED ELSE CONDITION {nenv.symenv.constraints}")
        for eif in ast["elseifs"]:
            nenv.symenv.constraints.append(Not(evalExpression(eif["cond"], env)))
        if nenv.symenv.sat():
            print(f"TAKING ELSE PATH: {nenv.symenv.constraints}")
            e.phpEval(ast["else"], nenv)


def evalElseIf(ast: Dict, env: Environment):
    c = evalExpression(ast["cond"], env)
    if satisfiable(c):
        nenv = env.fork()
        nenv.symenv.constraints.append(c)
        e.phpEvalAst(ast["stmts"], env)


def evalElse(ast: Dict, env: Environment):
    print(env.symenv.constraints)
    e.phpEvalAst(ast["stmts"], env)


def satisfiable(exp: ExprRef):
    s = Solver()
    s.add(exp)
    return s.check() == sat
