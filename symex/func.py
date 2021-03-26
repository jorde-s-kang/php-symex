import z3
import symex.expression as exp
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
        e.phpEvalAst(self.body, env)

def define(ast, env):
    fn = phpFunction(ast, env)
    phpFunctions[ast["name"]["name"]] = fn


def parseParam(ast, env):
    return ast["name"]
