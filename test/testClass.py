from .util import Capturing
import sys
sys.path.insert(0, "/home/jorde/proj/fyp/src/")

import symex.evaluation as e
import unittest

class TestClass(unittest.TestCase):

    def test_propfetch(self):
        with Capturing() as output:
            e.phpEvalInline("<?php class Fruit {public $name; public $color; function set_name($name) { $this->name = $name; } function test() { echo 'yes';}}; $f = Fruit(); $f->color = 'test';  echo $f->color;;")
        self.assertEqual(output[0], "test")

    def test_methodcall(self):
        with Capturing() as output:
            e.phpEvalInline("<?php class Fruit {public $name; public $color; function set_name($name) { $this->name = $name; } function test($a) { echo $a;}}; $f = Fruit(); $f->color = 'test';  $f->test('yes');")
        self.assertEqual(output[0], "yes")



