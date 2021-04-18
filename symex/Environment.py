import copy
from symex.SymbolicEnvironment import SymbolicEnvironment
from symex.UnknownVal import UnknownVal

class Environment:
    def __init__(self, p=None):
        self.env: dict = dict()
        self.parent = p
        self.symenv = SymbolicEnvironment(self)
        self.escapedStrings = []
        if self.parent is None:
                self.define("_COOKIE", UnknownVal())
                self.define("_SERVER", UnknownVal())
                self.define("_SESSION", UnknownVal())


    def __str__(self):
        return f"{self.env}\n{self.symenv}"
        
    def lookup(self, key: str, sym = False):
        try:
            out = self.env[key]
            return out
        except KeyError:
            try:
                self.symenv.symValues[key]
            except KeyError:
                if self.parent is not None:
                    out = self.parent.lookup(key, sym)
                    return out
            return None

    def __envcheck__(self, key: str) -> bool:
        try:
            a = self.env[key]
            return True
        except KeyError:
            return False
        except AttributeError:
            return false

    def fork(self):
        e = Environment(self)
        e.symenv = copy.deepcopy(self.symenv)
        # print(f"NEW SYMENV CONSTRAINTS: {e.symenv.constraints}")
        return e
        
    def define(self, key: str, val: object):
        found = False
        curr = self
        while curr is not None:  # linked list search
            if curr.__envcheck__(key):
                curr.env[key] = val
                found = True
                break
            curr = curr.parent
        if not found:
            self.env[key] = val            
