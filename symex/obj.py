import symex.expression as expr
import symex.func as func
from symex.Environment import Environment

from typing import Dict

class phpClass:
    def __init__(self, ast: Dict, env: Environment):
        self.name       = ast["name"]["name"]
        self.properties = {}
        self.methods    = {}
        props = [x for x in ast["stmts"] if x["nodeType"] == "Stmt_Property"]
        meths = [x for x in ast["stmts"] if x["nodeType"] == "Stmt_ClassMethod"]
        props = list(map(lambda x: evalProperty(x, env), props))
        meths = list(map(lambda x: evalMethod(x, env), meths))
        for i in props:
            self.properties[i[0]] = i[1]
        for i in meths:
            self.methods[i[0]] = i[1]
        print(f"properties: {self.properties}\n methods {self.methods}")


def evalProperty(ast, env):
    if ast == None:
        return [ast["props"][0]["name"]["name"], None]
    else:
        return [ast["props"][0]["name"]["name"], expr.evalExpression(ast["props"][0]["default"], env)]

# def evalMethod(ast, env):
#     return [ast["name"]["name"], func.PhpFunction(ast, env, builtin=False)]


def genClass(ast, env):
    name = ast["name"]["name"]
    stmts = [evalClassProp(stmt, env) for stmt in ast["stmts"]]
    d = {}
    for s in stmts:
        d[s[0]] = s[1]
    return type(name, (), d)
    

def evalClassProp(ast, env):
    if ast["nodeType"] == "Stmt_ClassMethod":
        return evalMethod(ast, env)
    elif ast["nodeType"] == "Stmt_Property":
        return evalProperty(ast, env)


def evalProperty(ast, env):
    if ast == None:
        return [ast["props"][0]["name"]["name"], None]
    else:
        return [ast["props"][0]["name"]["name"], expr.evalExpression(ast["props"][0]["default"], env)]
    
def evalMethod(ast, env):
    return [ast["name"]["name"], func.PhpFunction(ast, env)]
