import subprocess
import z3
import ast
import symex.expression as exp
import symex.evaluation as e
from symex.Environment import Environment
import symex.stdlib.encoding as encoding
import symex.stdlib.mysql as mysql
import symex.stdlib.varfuns as varfuns
import symex.stdlib.PDO as pdo
import symex.stdlib.mysqli as mysqli
from symex.UnknownVal import UnknownVal
phpFunctions = {}
escapedStrings = list()


class PhpFunction:
    def __init__(self, ast, env, mode=1):
        """
        mode:
        0 - user defined
        1 - builtin
        2 - unrecognized
        """
        self.mode = mode        
        if self.mode == 0:
            self.params  = [p["var"]["name"] for p in ast["params"]]
            self.body    = ast["stmts"]
        elif self.mode == 1:
            self.body = ast
        elif self.mode == 2:
            self.name = ast

    def unknown(self, *args, env=None):
        print(f"running unknown function: {self.name}")
        scalars = True
        for a in args:
            scalars = type(a) in [int, str, float, bool]
        if scalars:
            cmd = f"echo {self.name}("
            for arg in args[1:]:
                if type(arg) == str:
                    cmd += "'"
                    cmd += arg
                    cmd += "'"
                else:
                    cmd += str(arg)
                cmd += ","
        else:
            return UnknownVal()
                
            cmd += ");"
            # print(cmd)
            proc = subprocess.Popen(["php", "-r", cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if stderr != b'':
                print(stderr)
            out = str(stdout)[2:][:-1]
            try:
                return ast.literal_eval(out)
            except ValueError: #String
                return out
            

    def run(self, params, env):
        i = 0
        if self.mode == 0:
            env = env.fork()
            while i < len(params):
                p = self.params[i]
                env.define(p, params[i])
                i += 1            
            return e.phpEvalAst(self.body, env)
        elif self.mode == 1:
            return self.body(*params, env)
        elif self.mode == 2:
            return self.unknown(self.name, *params, env=env)


def define(ast, env):
    fn = PhpFunction(ast, env)
    phpFunctions[ast["name"]["name"]] = fn

def parseParam(ast, env):
    return ast["name"]


def addBuiltIn(name, fn):
    phpFunctions[name] = PhpFunction(fn,Environment(), mode=1)

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
