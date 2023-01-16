import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'code/translator'))

from lexer import tokenize
from syntaxer import SyntaxAnalyzer

unexpected_token = [
    '''a = 5 + math.sin(print(5))''',
    '''math.sin(5''',
    '''while: 6''',
    '''if 5 > 0: print(6)''',
    '''b + (a - (7)''',    
    ]

class TestSyntaxer(unittest.TestCase):

    def test_unexpected_token(self):
        for code in unexpected_token:
            with self.assertRaises(SyntaxError):
                tokens = tokenize(code)
                analyzer = SyntaxAnalyzer(tokens)
                analyzer.parse()


if __name__ == '__main__':
    unittest.main()