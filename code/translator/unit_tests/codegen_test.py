import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'code/translator'))

from lexer import tokenize
from syntaxer import SyntaxAnalyzer
from semanalyzer import SemanticAnalyzer
from codegen import CodeGenerator

code_pair = [
    ('''a = 5''', '''let a;\na = 5;\n'''),
    ('''while True:\n\tprint(1 + 2 * 7)''', '''while (true) {\n\tconsole.log(1 + 2 * 7);\n}\n'''),
    ('''a = math.sin(0)''', '''let a;\na = Math.sin(0);\n'''),
    ('''b = 8\nif b and 4:\n\tb = b - 1\nelse:\n\tc = b - 2''', '''let b;\nb = 8;\nif (b && 4) {\n\tb = b - 1;\n}\nelse {\n\tlet c;\n\tc = b - 2;\n}\n'''),
    ('''5 or 7''', '''5 || 7\n'''),
    ('''-5.896''', '''-5.896\n'''),
    ]


class TestSemAnalyzer(unittest.TestCase):

    def test_reserved_name(self):
        for input, output in code_pair:            
            tokens = tokenize(input)
            analyzer = SyntaxAnalyzer(tokens)
            syntaxTree = analyzer.parse()
            SemanticAnalyzer().check(syntaxTree)
            out = CodeGenerator().genJavaScript(syntaxTree)
            self.assertEqual(out, output)


if __name__ == '__main__':
    unittest.main()