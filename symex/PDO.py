import re
import z3
import symex.func

class PhpPDO:
    def __init__(self, dsn="", username="", passwd="", options=[]):
        return None

    def exec(self, statement, env):
        if type(p) == list:
            for p in string:
                if type(p) == z3.SeqRef:
                    if not env.escaped(p):
                        print("WARNING: UNESCAPED STRING passed to database query, potential SQL injection vulnerability!")
    
    def prepare(self, statement, env):
        return PhpPDOStatement(statement, env)

    def query(self, statement, env):
        self.exec(statement, env)

class PhpPDOStatement:
    def __init__(self, qstring, env):
        if type(qstring) == str:
            self.query = self.__parse__(qstring)
        elif type(qstring) == list:
            qlist = []
            for i in qstring:
                if type(i)  == str:
                    qlist.append(self.__parse__(i))
                else:
                    qlist.append(i)
            self.query = []
            for i in qlist:
                if type(i) == list:
                    for j in i:
                        self.query.append(j)
                else:
                    self.query.append(i)                    
        

    def __parse__(self, qstring):
        out = []
        curstring = ""
        escape = False
        index = 1
        i = 0 
        while i < len(qstring):
            c = qstring[i]
            if c == "\\":
                escape = True
            elif c == "?" and not escape:
                out.append(curstring)
                curstring = ""
                out.append(PhpPDOKeyword(index))
                index += 1
            elif c == ":" and not escape:
                kname = ""
                ch = qstring[i]
                while ch != " " and not escape:
                    kname += ch
                    i += 1
                    ch = qstring[i]
                out.append(curstring)
                curstring = ""
                out.append(PhpPDOKeyword(kname))
            else:
                escape = False
                curstring += c
            i += 1
        out.append(curstring)
        return out
 
    def bindParam(self, param, var, dtype, env):
        return 0

    def BindValue():
        return 0
    def bindColumn():
        return 0
    def execute():
        return 0
    def fetch():
        return 0
    def fetchAll():
        return 0

class PhpPDOKeyword:
    def __init__(self, name):
        self.name = name
        self.value = None
