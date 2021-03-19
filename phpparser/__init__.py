import subprocess
from requests import get, Response
import json
from typing import List


class Parser:
    def __init__(self, p: int = 8888):
        self.port = p
        self.proc = subprocess.Popen(["php",
                                      "-S",
                                      f"localhost:{self.port}"],
                                     cwd="/home/jorde/proj/fyp/src/phpparser",
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

    def __req__(self, command: str, data: str) -> str:
        r: Response = get(f"http://localhost:{self.port}/parser.php",
                          params={"mode": command,
                                  "data": data})
        return r.text

    def parse_file(self, fname: str) -> List:
        return json.loads(self.__req__("file", fname))

    def parse_inline(self, exp: str) -> List:
        return json.loads(self.__req__("inline", exp))
