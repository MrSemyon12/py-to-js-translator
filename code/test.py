import lexer
import syntaxer
import semanalyzer

code = '''
while 4 + 4:
    if True:
        a = 0
    else:
        while True:
            a = 0
'''


tokens = list(lexer.tokenize(code))
for token in tokens:
    print(token)
analyzer = syntaxer.SyntaxAnalyzer(tokens)
syntaxTree = analyzer.parse()

print(analyzer.getTree(syntaxTree))
semanalyzer.SemanticAnalyzer().check(syntaxTree)
