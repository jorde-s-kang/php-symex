from .util import Capturing
import sys
sys.path.insert(0, "/home/jorde/proj/fyp/src/")

import symex.evaluation as e
import unittest

class TestExpression(unittest.TestCase):

    def test_binop(self):
        with Capturing() as output:
            e.phpEvalInline("<?php echo True && (True || False);")
        self.assertEqual(output[0], "And(True, Or(True, False))")
        with Capturing() as output:
            e.phpEvalInline("<?php echo 1 + (4 / 2);")
        self.assertEqual(output[0], "3.0")

    def test_variable(self):
        with Capturing() as output:
            e.phpEvalInline("<?php $a = 1; echo $a;")
        self.assertEqual(output[0], "1")

    def test_array(self):
        with Capturing() as output:
            e.phpEvalInline("<?php $a = [1,2,3,4]; echo $a[2];")
        self.assertEqual(output[0], "3")

if __name__ == '__main__':
    unittest.main()
