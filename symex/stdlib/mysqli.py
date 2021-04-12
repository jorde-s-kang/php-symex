import symex.stdlib.PDO as pdo

class PhpMysqli(pdo.PhpPDO):
    def __init__(self):
        return None

    def real_query(statement, env):
        super.exec(statement, env)

    def query(self, statement, env):
        super.exec(statement, env)

    def prepare(self, statement, env):
        return PhpMysqliStatement(statement, env)

    def real_escape_string(self, string, env):
        env.escapedStrings.append(string)
        return string

class PhpMysqliStatement(pdo.PhpPDOStatement):
    def __init__(self, qstring, env):
        super.__init__(qstring, env)

    def bind_param(param, var, dtype, env):
        super.bindParam(param, var, dtype, env)
