import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'code/translator'))

from lexer import tokenize
from syntaxer import SyntaxAnalyzer
from semanalyzer import SemanticAnalyzer

undeclared_variable = '''a = b + 1'''
unexpected_else = '''if 5 > 0:
    else:
        print(1)
if True:
    print(True)
else:
    print(False)'''

class TestSemAnalyzer(unittest.TestCase):

    def test_undeclared_variable(self):
        with self.assertRaises(NameError):
            tokens = tokenize(undeclared_variable)
            analyzer = SyntaxAnalyzer(tokens)
            syntaxTree = analyzer.parse()
            SemanticAnalyzer().check(syntaxTree)

    def test_unexpected_else(self):
        with self.assertRaises(SyntaxError):
            tokens = tokenize(unexpected_else)
            analyzer = SyntaxAnalyzer(tokens)
            syntaxTree = analyzer.parse()
            SemanticAnalyzer().check(syntaxTree)


if __name__ == '__main__':
    unittest.main()