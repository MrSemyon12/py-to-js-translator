import lexer
import syntaxer
import semanalyzer
import codegen

code = '''
a = 5 + math.sin(5)
if a and abs(5):
    print(5)
else:
    while True:
        if 4 or 0 and 5:
            a = a- 1
        else:
            print(1)
    a = a - 5 + 6 / (4 - math.sqrt(7 + 0))
    b = a
print(6)
'''


tokens = list(lexer.tokenize(code))
for token in tokens:
    print(token)

analyzer = syntaxer.SyntaxAnalyzer(tokens)
syntaxTree = analyzer.parse()
textTree = analyzer.getTextTree(syntaxTree)
print(textTree)

semanalyzer.SemanticAnalyzer().check(syntaxTree)

output = codegen.CodeGenerator().genJavaScript(syntaxTree)
print(output)
