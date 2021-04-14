import z3
import symex.expression as exp
import symex.evaluation as e
from symex.Environment import Environment
import symex.stdlib.encoding as encoding
import symex.stdlib.mysql as mysql
import symex.stdlib.varfuns as varfuns
import symex.stdlib.PDO as pdo
import symex.stdlib.mysqli as mysqli
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
                env.define(p, params[i])
                i += 1
            return e.phpEvalAst(self.body, env)

def define(ast, env):
    fn = PhpFunction(ast, env)
    phpFunctions[ast["name"]["name"]] = fn

def parseParam(ast, env):
    return ast["name"]


def addBuiltIn(name, fn):
    phpFunctions[name] = PhpFunction(fn,Environment(), builtin=True)

def addConstructor(name, fn):
    global phpFunction
    phpFunctions[name] = fn


# Encoding
addBuiltIn("htmlspecialchars",    encoding.phpEncodeString)
addBuiltIn("htmlentities",        encoding.phpEncodeString)
addBuiltIn("md5",                 encoding.phpEncodeString)
addBuiltIn("mysql_escape_string", encoding.phpEncodeString)

# Mysql functional interface
addBuiltIn("mysql_query",   mysql.phpMysqlQuery)
addBuiltIn("mysql_connect", mysql.MysqlConnection)

# Database object interfaces
addConstructor("PDO", pdo.PhpPDO)
addConstructor("mysqli", mysqli.PhpMysqli)

# Variable functions
addBuiltIn("gettype", varfuns.varType)
addBuiltIn("isset",  varfuns.phpisset)
addBuiltIn("is_int", varfuns.phpIsInt)
addBuiltIn("is_integer", varfuns.phpIsInt)
addBuiltIn("is_long", varfuns.phpIsInt)
addBuiltIn("is_double", varfuns.phpIsFloat)
addBuiltIn("is_float", varfuns.phpIsFloat)
