import z3
from .util import Capturing
import sys
sys.path.insert(0, "/home/jorde/proj/fyp/src/")

import symex.evaluation as e
import unittest

class TestCond(unittest.TestCase):
    
    def test_if(self):
        a = z3.Int("a")
        with Capturing() as output:
            e.phpEvalInline("<?php if ($_GET['a'] > 5) { echo 'if taken';}",
                            getVars={'a': a},
                            constraints=[a > 5])
        self.assertEqual(output[0], "if taken")

    def test_elif(self):
        a = z3.Int("a")
        with Capturing() as output:
            e.phpEvalInline("<?php if ($_GET['a'] < 4) { echo 'if taken';} elseif ($_GET['a'] == 6) { echo 'elif1';} elseif ($_GET['a'] == 7) { echo 'elif2'; } elseif ($_GET['a'] == 1) { echo 'elif3';}",
                            getVars={'a': a},
                            constraints=[a > 5])
        self.assertEqual(output[0], "elif1")
        self.assertEqual(output[1], "elif2")

    def test_else(self):
        a = z3.Int("a")
        with Capturing() as output:
            e.phpEvalInline("<?php if ($_GET['a'] > 5) { echo 'if taken';} else {echo 'else taken';}",
                            getVars={'a': a},
                            constraints=[a < 5])
        self.assertEqual(output[0], "else taken")

    def test_both(self):
        a = z3.Int("a")
        with Capturing() as output:
            e.phpEvalInline("<?php if ($_GET['a'] > 5) { echo 'if taken';} else {echo 'else taken';}",
                            getVars={'a': a})
        self.assertEqual(output[0], "if taken")
        self.assertEqual(output[1], "else taken")
