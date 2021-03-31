import z3
import symex.expression as exp
import symex.evaluation as e
from symex.Environment import Environment
import symex.PDO as PDO
phpFunctions = {}
escapedStrings = list()



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
            return self.body(*params, env)
        else:
            env = env.fork()
            while i < len(params):
                p = self.params[i]
                env.define(p["name"], params[i])
                i += 1
            return e.phpEvalAst(self.body, env)

def define(ast, env):
    fn = phpFunction(ast, env)
    phpFunctions[ast["name"]["name"]] = fn

def parseParam(ast, env):
    return ast["name"]


def addBuiltIn(name, fn):
    phpFunctions[name] = PhpFunction(fn,Environment(), builtin=True)

def addConstructor(name, fn):
    phpFunctions[name] = fn

def phpHtmlSpecialChars(string,env):
    print(f"escaped: {string}")
    env.escapedStrings.append(string)
    return string

addBuiltIn("htmlspecialchars", phpHtmlSpecialChars)
addBuiltIn("htmlentities", phpHtmlSpecialChars)

def phpMysqliQuery(conn, string, env):
    for p in string:
        if type(p) == z3.SeqRef:
            if p not in env.escapedStrings:
                print("WARNING: UNESCAPED STRING passed to database query, potential SQL injection vulnerability!")
            print("WARNING: Using non-parameterized queries with user input!")
addBuiltIn("mysqli_query", phpMysqliQuery)

addConstructor("PDO", PDO.PhpPDO)
# Localise to functions that do database functions and expand to
# functions that call those functions
