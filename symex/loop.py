from typing import Dict
from .Environment import Environment
from z3 import Solver, sat
import symex.evaluation as e
from symex.expression import evalExpression


def evalWhile(ast: Dict, env: Environment):
    en = Environment(env)
    s = Solver()
    c = ast["cond"]
    so.add(evalExpression(c, so, env))
    while so.check() == sat:
        print(so)
        e.phpEvalAst(ast["stmts"], en)
        so = Solver()
        so.add(evalExpression(c, en))


def evalFor(ast: Dict, s: Solver, env: Environment):
    en = Environment(env)
    so = Solver()
    init = evalExpression(ast["init"][0], so, en)
    so.add(evalExpression(ast["cond"][0], so, en))
    while so.check() == sat:
        e.phpEvalAst(ast["stmts"], so, en)
        evalExpression(ast["loop"][0], so, en)
        so = Solver()
        so.add(evalExpression(ast["cond"][0], so, en))

def evalForEach(ast: Dict, s: Solver, env: Environment):
    arr = env.lookup(evalExpression(ast["expr"], s, env))
    val = ast["valueVar"]["name"]
    for term in arr:
        en = Environment(env)
        en.define("val", term)
        e.phpEvalAst(ast["stmts"])
