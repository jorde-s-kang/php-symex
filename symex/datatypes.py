import z3


def getValue(self):
        s = z3.Solver()
        for c in self.constraints:
            s.add(c)
        s.check()
        return s.model()[self.val]

def addConstraints(self, cons):
    for c in cons:
        self.constraints.append(c)

def genType(name, fn):
    def initFun(self, name):
        self.constraints = []
        self.val = fn(name)
    return type(name,
                (),
                {"__init__": initFun,
                 "getValue": getValue,
                 "addConstraints": addConstraints})

String = genType("String", z3.String)
Int    = genType("Int", z3.Int)
Bool   = genType("Bool", z3.Bool)
Real   = genType("Real", z3.Real)
