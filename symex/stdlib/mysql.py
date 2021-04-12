import z3
from symex.Environment import Environment

def phpMysqlQuery(conn, string, env):
    print(f"query made: {string}")
    for p in string:
        if type(p) == z3.SeqRef:
                print(f"[!] UNESCAPED STRING passed to database query, potential SQL injection vulnerability with input variable {p}!")

def phpMysqlDBQuery(db, query, conn, env):
    phpMysqlQuery(conn, query, env)

class MysqlConnection:
    def __init__(self, server="", username="", password="", new_link=None, flags=None):
        self.server = server
        self.username = username
        self.password = password
        self.new_link = new_link
        self.flags = flags
