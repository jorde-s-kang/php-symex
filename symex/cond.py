from z3 import Solver, ExprRef, sat, Not, And
from symex.Environment import Environment
from symex.expression import evalExpression
import symex.evaluation as e
import copy
from typing import Dict


def evalConditional(ast: Dict, env: Environment, c: ExprRef):
    print(f"FORK @ LINE {ast['attributes']['startLine']} : {ast['nodeType']} : {c}")
    nenv = env.fork()
    nenv.symenv.constraints.append(c)
    print(f"FORK CONDITIONS {nenv.symenv.constraints}")
    if nenv.symenv.sat():
        print("SATISFIABLE, TAKING FORK")
        e.phpEvalAst(ast["stmts"], nenv)
    else:
        print("UNSATISFIABLE")
    

def evalIf(ast: Dict, env: Environment) -> ExprRef:
    c: ExprRef = evalExpression(ast["cond"], env)
    evalConditional(ast, env, c)
    # if nenv.symenv.sat():
    #     nenv = env.fork()
    #     nenv.symenv.constraints.append(c)
    #     print(f"TAKING IF PATH: {nenv.symenv.constraints}")
    #     e.phpEvalAst(ast["stmts"], nenv)
    try:
        e.phpEvalAst(ast["elseifs"], env)
    except KeyError:
        pass
    if ast["else"] is not None:
        conds = [Not(evalExpression(c["cond"], env)) for c in ast["elseifs"]]
        conds.append(Not(c))
        elsec = And(*conds)
        evalConditional(ast["else"], env, elsec)
        # print("else fork")
        # nenv = env.fork()
        # print(f"FORKED ELSE CONSTRAINTS: {nenv.symenv.constraints}")
        # nenv.symenv.constraints.append(Not(c))
        # print(f"ADDED ELSE CONDITION {nenv.symenv.constraints}")
        # for eif in ast["elseifs"]:
        #     nenv.symenv.constraints.append(Not(evalExpression(eif["cond"], env)))
        # if nenv.symenv.sat():
        #     print(f"TAKING ELSE PATH: {nenv.symenv.constraints}")
        #     e.phpEval(ast["else"], nenv)


def evalElseIf(ast: Dict, env: Environment):
    evalIf(ast, env)


def evalElse(ast: Dict, env: Environment):
    print(env.symenv.constraints)
    e.phpEvalAst(ast["stmts"], env)


def satisfiable(exp: ExprRef):
    s = Solver()
    s.add(exp)
    return s.check() == sat
