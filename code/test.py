import lexer
import syntaxer
import semanalyzer
import codegen

code = '''
while 4 + 4:
    if True:
        a = 0
    else:
        while True:
            a = 0
'''


tokens = list(lexer.tokenize(input))
for token in tokens:
    print(token)

analyzer = syntaxer.SyntaxAnalyzer(tokens)
syntaxTree = analyzer.parse()
textTree = analyzer.getTextTree(syntaxTree)
print(textTree)

semanalyzer.SemanticAnalyzer().check(syntaxTree)

output = codegen.CodeGenerator().genJavaScript(syntaxTree)
print(output)
