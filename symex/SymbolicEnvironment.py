from z3 import *

class SymbolicEnvironment:
    def __init__(self, env):
        self.symValues = dict()
        self.constraints = Solver()

    def __str__(self):
        return f"Symbolic Environment: {self.symValues}, {self.constraints}"

    def lookup(self, key: str):
        return self.symValues[key]

    def define(self, key: str, val: object):
        self.symValues[key] = val

    def getModel(self):
        s = copy.deepcopy(self.constraints)
        for key, val in self.symValues.items():
            s.add(val)
        s.check()
        return s.model()

    
