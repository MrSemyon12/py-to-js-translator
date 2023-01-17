import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'code/translator'))

from lexer import tokenize

unsupported_token = '$[]{^}\|&?;%@!`~'

reserved_name = [
    '''a = true''',
    '''a = false''',
    '''Math.sin(6)''',
    '''console = 9''',
    '''let = console''',
    ]

class TestLexer(unittest.TestCase):

    def test_unsupported_token(self):
        for token in list(unsupported_token):            
            with self.assertRaises(SyntaxError):            
                tokenize(token)

    def test_reserved_name(self):
        for code in reserved_name:
            with self.assertRaises(NameError):
                tokenize(code)
                

if __name__ == '__main__':
    unittest.main()
