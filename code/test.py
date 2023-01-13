import lexer
import syntaxer

code = ''''''


tokens = list(lexer.tokenize(code))
for token in tokens:
    print(token)
analyzer = syntaxer.SyntaxAnalyser(tokens)
syntaxTree = analyzer.parse()

print(analyzer.getTree(syntaxTree))
