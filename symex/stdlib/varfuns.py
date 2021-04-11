import z3

def phpisset(var, env):
    return env.lookup(var) is not None

def varType(var, env):
    return type(env.lookup(var))

def typeFun(a, b):
    def retFun(var, env):
        t = varType(var, env)
        return t == a or t == b
    return retFun

phpIsInt = typeFun(int, z3.Int)
phpIsFloat = typeFun(float, z3.Float)
phpIsString = typeFun(str, z3.String)
