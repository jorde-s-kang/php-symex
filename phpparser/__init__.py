import re
import subprocess
import json
from typing import List
import time
import os

class ParseError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def parse(cmd, string):
    """
    Passes the string and command to the PHP parser.
    Args:
        cmd (str): 'inline' or 'file' to denote what the second argument is
        string (str): either inline PHP code or a file path depending on the cmd
    """
    proc = subprocess.Popen(["php",
                             "/home/jorde/proj/fyp/src/phpparser/parser.php",
                             cmd,
                             string],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    out = str(stdout)[2:][:-1]
    if(out[0] != "["):
        raise ParseError(str(stdout)[2:])
    else:
        return json.loads(out.replace("\\", "\\\\").replace("\\\"", "\\\\\""))
    
def parseInline(string):
    """
    Parse inline PHP code.
    Args:
        string (str): Inline PHP code
    """
    return parse("inline", string)

def parseFile(string):
    """
    Parse A PHP file.
    Args:
        string (str): A path to a PHP file
    """
    return parse("file", string)
