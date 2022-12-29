import translator.lexer.lexicalAnalizer as la
import translator.IOpackage.ReadWriteClass as IO
from translator.syntaxer.syntaxanalizer import SyntaxAnalizer
from translator.syntaxer.sintaxunit import SyntaxUnit
from translator.syntaxer.rule import Rule
from translator.syntaxer.grammar import Grammar
from translator.syntaxer.ATS import SyntacticalTree
from translator.semanticaltree.operationtree import SyntacticsStructure
from translator.semanticaltree.semanticalanalizer import SemanticalAnalyzer
from translator.codegenerator.codegenerator import CodeGenerator


class Tester:
    def __init__(self):
        self.run()

    def test(self, number):
        sa = SyntaxAnalizer()
        code = IO.read("Test "+str(number))
        tokens = la.parse(code)
        print(la.lextableToString(tokens.tokens_array))
        table = sa.earley(rule=sa.grammatic.PROGRAMM,
                          text=la.lextableToString(tokens.tokens_array))
        parsed = sa.right_parsing(table)
        tree = SyntacticalTree(parsed)
        tree.printTree()
        IO.writeSyntaxTree(tree, "Test " + str(number))
        operationtree = SyntacticsStructure(tree)
        operationtree.printast()
        IO.writeOperationTree(operationtree, "Test "+str(number))
        sema = SemanticalAnalyzer(operationtree)
        translator = CodeGenerator(operationtree, sema.variables)
        translator.translate(operationtree.root)
        print(translator.output)
        IO.writeCode(translator.output, "Test " + str(number))

    def run(self):
        for i in range(2):
            self.test(i)
