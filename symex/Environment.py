import copy
from symex.SymbolicEnvironment import SymbolicEnvironment

class Environment:
    def __init__(self, p=None):
        self.env: dict = dict()
        self.parent = p
        self.symenv = SymbolicEnvironment(self)
        self.escapedStrings = []

    def __str__(self):
        return f"{self.env}\n{self.symenv}"
        
    def lookup(self, key: str, sym = False):
        try:
            out = None
            if sym:
                out = self.symenv.lookup(key)
            else:
                out = self.env[key]
            return out
        except KeyError:
            if self.parent is not None:
                out = self.parent.lookup(key, sym)
                return out

    def __envcheck__(self, key: str) -> bool:
        try:
            return True
        except KeyError:
            return False

    def fork(self):
        e = Environment(self)
        e.symenv = copy.deepcopy(self.symenv)
        # print(f"NEW SYMENV CONSTRAINTS: {e.symenv.constraints}")
        return e
        
    def define(self, key: str, val: object, sym=False):
        found = False
        curr = self
        while curr is not None:  # linked list search
            if curr.__envcheck__(key):
                if sym:
                    curr.symenv.define(key, val)
                else:
                    curr.env[key] = val
                found = True
                break
            curr = curr.parent
        if not found:
            if sym:
                self.symenv.define(key, val)
            else:
                curr.env[key] = val            
