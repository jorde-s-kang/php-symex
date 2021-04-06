from .util import Capturing
import sys
sys.path.insert(0, "/home/jorde/proj/fyp/src/")

import symex.evaluation as e
import unittest

class TestFunction(unittest.TestCase):

    def test_function(self):
        with Capturing() as output:
            e.phpEvalInline("<?php function testfun($a){ echo $a; } echo testfun(1);")
        self.assertEqual(output[0], "1")

if __name__ == '__main__':
    unittest.main()
