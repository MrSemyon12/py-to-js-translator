import lexer
import syntaxer

code = '''a = (321.7 + value) * (7 - (8 / 9))


b = a / 7
'''


tokens = list(lexer.tokenize(code))
analyzer = syntaxer.SyntaxAnalyser(tokens)
syntaxTree = analyzer.parse()

print(analyzer.getTree(syntaxTree))
