from translator.lexer import lexicalAnalizer as la
from translator.IOpackage import ReadWriteClass as IO
from translator.syntaxer.syntaxanalizer import SyntaxAnalizer
from translator.syntaxer.sintaxunit import SyntaxUnit
from translator.syntaxer.rule import Rule
from translator.syntaxer.grammar import Grammar
from translator.syntaxer.ATS import SyntacticalTree
from translator.semanticaltree.operationtree import SyntacticsStructure
from translator.semanticaltree.semanticalanalizer import SemanticalAnalyzer
from translator.codegenerator.codegenerator import CodeGenerator
from translator.test.RunTests import Tester


def test(path):
    sa = SyntaxAnalizer()
    code = IO.read(path)
    tokens = la.parse(code)
    print(la.lextableToString(tokens.tokens_array))
    table = sa.earley(rule=sa.grammatic.PROGRAMM,
                      text=la.lextableToString(tokens.tokens_array))
    parsed = sa.right_parsing(table)
    tree = SyntacticalTree(parsed)
    tree.printTree()
    IO.writeSyntaxTree(tree, path)
    operationtree = SyntacticsStructure(tree)
    operationtree.printast()
    IO.writeOperationTree(operationtree, path)
    sema = SemanticalAnalyzer(operationtree)
    translator = CodeGenerator(
        operationtree, sema.rootscope, sema.maxscopelevel)
    translator.translate(operationtree.root)
    print(translator.output)
    IO.writeCode(translator.output, path)


if __name__ == '__main__':
    test()
