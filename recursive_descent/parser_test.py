import unittest
from parser import parse


class TestParsingResult(unittest.TestCase):
    
    def setUp(self):
        self.case_one = '2 * (2 - 3)'
        self.case_two = '3 * ( 2 / 2)'
        self.case_three = '(1 * 3 + 2)  - (4 / 1 + 3) * 2'

    def test_parsing_result(self):
        self.assertTrue(parse(self.case_one), -2)
        self.assertTrue(parse(self.case_two), 3)
        self.assertTrue(parse(self.case_three), -9)


if __name__ == "__main__":
    unittest.main()
