from typing import Dict
from .Environment import Environment
from z3 import Solver, sat
import symex.evaluation as e
import symex.expression as expr


def evalWhile(ast: Dict, env: Environment):
    en = Environment(env)
    so = Solver()
    c = ast["cond"]
    so.add(expr.evalExpression(c, env))
    while so.check() == sat:
        print(so)
        e.phpEvalAst(ast["stmts"], en)
        so = Solver()
        so.add(expr.evalExpression(c, en))


def evalFor(ast: Dict, s: Solver, env: Environment):
    en = Environment(env)
    so = Solver()
    init = expr.evalExpression(ast["init"][0], so, en)
    so.add(expr.evalExpression(ast["cond"][0], so, en))
    while so.check() == sat:
        e.phpEvalAst(ast["stmts"], so, en)
        expr.evalExpression(ast["loop"][0], so, en)
        so = Solver()
        so.add(expr.evalExpression(ast["cond"][0], so, en))

def evalForEach(ast: Dict, s: Solver, env: Environment):
    arr = env.lookup(expr.evalExpression(ast["expr"], s, env))
    val = ast["valueVar"]["name"]
    for term in arr:
        en = Environment(env)
        en.define("val", term)
        e.phpEvalAst(ast["stmts"])
