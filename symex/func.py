import z3
import symex.expression as exp
import symex.evaluation as e
from symex.Environment import Environment

phpFunctions = {}
escapedStrings = list()



# includes (?)
# Classes
# Function definition
# String related functions
# PDO, mysqli related functions
# Can skip other function calls probably


class PhpFunction:
    def __init__(self, ast, env, builtin=False):
        self.builtin = builtin        
        if not self.builtin:
            self.params  = [p["var"]["name"] for p in ast["params"]]
            self.body    = ast["stmts"]
        else:
            self.body = ast


    def run(self, params, env):

        i = 0
        if(self.builtin):
            self.body(*params, env)
        else:
            env = env.fork()
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


def addBuiltIn(name, fn):
    phpFunctions[name] = PhpFunction(fn,Environment(), builtin=True)

def phpHtmlSpecialChars(string,env):
    print(f"escaped: {string}")
    env.escapedStrings.append(string)
    return env

addBuiltIn("htmlspecialchars", phpHtmlSpecialChars)
addBuiltIn("htmlentities", phpHtmlSpecialChars)

# Localise to functions that do database functions and expand to
# functions that call those functions
