import z3
from symex.expression import evalExpression
import symex.evaluation as e
phpFunctions = {}




# includes (?)
# Classes
# Function definition
# String related functions
# PDO, mysqli related functions
# Can skip other function calls probably


class phpFunction:
    def __init__(self, ast, env, builtin=False):
        print(ast["params"][0])
        self.params  = [p["var"]["name"] for p in ast["params"]]
        self.body    = ast["stmts"]
        self.builtin = builtin

    def run(self, params, env):
        env = env.fork()
        i = 0
        while i < len(params):
            p = self.params[i]
            env.define(p["name"], params[i])
            i += 1
        e.phpEvalAst(self.body)

def define(ast, env):
    fn = phpFunction(ast, env)
    print(ast["name"])
    phpFunctions[ast["name"]["name"]] = fn
    print(phpFunctions)


def parseParam(ast, env):
    return ast["name"]
