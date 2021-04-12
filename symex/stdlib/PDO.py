import re
import z3

class PhpPDO:
    def __init__(self, dsn="", username="", passwd="", options=[], env=None):
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
        bindValue(param, var)

    def bindValue(self, key, value):
        item = list(filter(lambda x: type(x) == PhpPDOKeyword and x.name == 1, self.query))[0]
        item.value = value

    def bindColumn():
        return 0
    def execute(self, *args, env=None):
        l = list(filter(lambda x: type(x) == z3.ExprRef or z3.ExprRef in type(x).__bases__, self.query))
        if len(l) > 0:
            print(f"SQL INJECTION VULNERABILITY, UNSANITIZED INPUT PASSED TO PREPARED STATEMENT\nVULNERABLE VARS: {l}")
    def fetch():
        return 0
    def fetchAll():
        return 0

class PhpPDOKeyword:
    def __init__(self, name):
        self.name = name
        self.value = None
