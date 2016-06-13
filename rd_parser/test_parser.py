import unittest
import copy
from parser import Var


class TestVarArithOperation(unittest.TestCase):
    
    def setUp(self):
        self.var1 = Var({'x': 2, 'y': 1}, 3)
        self.var2 = Var({'x': 5, 'y': 0, 'z': 5}, 10)

    def testAdd(self):
        self.assertEqual(self.var1 + self.var2, Var({'x': 7, 'y': 1, 'z': 5}, 13))
        self.assertEqual(self.var1 + 10, Var({'x': 2, 'y': 1}, 13))

    def testIAdd(self):
        tmp = copy.deepcopy(self.var1)
        tmp += self.var2
        self.assertEqual(tmp, Var({'x': 7, 'y': 1, 'z': 5}, 13))

    def testRAdd(self):
        self.assertEqual(-10 + self.var1, Var({'x': 2, 'y': 1}, -7))

    def testSub(self):
        self.assertEqual(self.var1 - self.var2, Var({'x': -3, 'y': 1, 'z': -5}, -7))
        self.assertEqual(self.var1 - (-2), Var({'x': 2, 'y': 1}, 5))

    def testISub(self):
        tmp = copy.deepcopy(self.var1)
        tmp -= self.var2
        self.assertEqual(tmp, Var({'x': -3, 'y': 1, 'z': -5}, -7))
        tmp = copy.deepcopy(self.var1)
        tmp -= 20
        self.assertEqual(tmp, Var({'x':2, 'y': 1}, -17))

    def testRSub(self):
        self.assertEqual(-20 - self.var1, Var({'x': -2, 'y': -1}, -23))

if __name__ == '__main__':
    unittest.main()
