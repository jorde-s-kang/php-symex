from z3 import *

class SymbolicEnvironment:
    def __init__(self, env):
        self.symValues = dict()
        self.constraints = list()

    def __str__(self):
        return f"Symbolic Environment: {self.symValues}, {self.constraints}"

    def lookup(self, key: str):
        return self.symValues[key]

    def define(self, key: str, val: object):
        self.symValues[key] = val

    def getModel(self):
        s = Solver()
        for c in constraints:
            s.add(c)
        s.check()
        return s.model()

    def sat(self):
        s = Solver()
        for c in self.constraints:
            s.add(c)
        return s.check() == sat
