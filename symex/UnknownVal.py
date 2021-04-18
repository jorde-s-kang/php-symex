class UnknownVal:
    def getVal(self, a):
        if type(a) == int or type(a) == float:
            return 1
        if type(a) == str:
            return ""
        if type(a) == bool:
            return True

    def __str__(self):
        return "Unknown value"

    def __add__(self, a):
        return self.getVal(a) + a
        
    def __mult__(self, a):
        return self.getVal(a) * a

    def __sub__(self, a):
        return self.getVal(a) - a
    
    def __truediv__(self, a):
        return self.getVal(a) / a

    def __or__(self, a):
        return self.getVal(a) or a

    def __invert__(self):
        return not True

    def __and__(self, a):
        return self.getVal(a) and a

    def __getitem__(self, a):
        return UnknownVal()
    
