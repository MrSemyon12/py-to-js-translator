import lexer
import syntaxer

code = '''abs(abs(4) * math.sin(5 + 8))'''


tokens = list(lexer.tokenize(code))
# for token in tokens:
#     print(token)
analyzer = syntaxer.SyntaxAnalyser(tokens)
syntaxTree = analyzer.parse()

print(analyzer.getTree(syntaxTree))
