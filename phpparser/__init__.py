import re
import subprocess
import json
from typing import List
import time
import os

# class Parser:
#     def __init__(self, p: int = 8888):
#         self.port = p
#         self.proc = subprocess.Popen(["php",
#                                       "-S",
#                                       f"localhost:{self.port}"],
#                                      cwd="/home/jorde/proj/fyp/src/phpparser",
#                                      stdout=subprocess.PIPE,
#                                      stderr=subprocess.PIPE)
#         time.sleep(1)
    
#     def __req__(self, command: str, data: str) -> str:
#                           params={"mode": command,
#                                   "data": data})
#         return r.text

#     def parse_file(self, fname: str) -> List:
#         return json.loads(self.__req__("file", fname))

#     def parse_inline(self, exp: str) -> List:
#         return json.loads(self.__req__("inline", exp))

#     def __del__(self):
#         self.proc.terminate()

#     def getdir(self):
#         print(os.getcwd())

class ParseError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def parse(*args):
    proc = subprocess.Popen(["php",
                             "/home/jorde/proj/fyp/src/phpparser/parser.php",
                             args[0],
                             args[1]],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    out = str(stdout)[2:][:-1]
    if(out[0] != "["):
        raise ParseError(str(stdout)[2:])
    else:
        return json.loads(out.replace("\\", "\\\\").replace("\\\"", "\\\\\""))
    
def parseInline(string):
    return parse("inline", string)

def parseFile(string):
    return parse("file", string)
