from flask import Flask, render_template, request, flash
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'code/translator'))

import codegen
import semanalyzer
import lexer
import syntaxer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smA8691BVVd2bq9iSzeAm2yW1GJJD0dE'

@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')
    output = ''
    textTree = ''
    tokens = ''

    if not input:
        return render_template('index.html', input='', output='', syntaxTree='', tokens='')

    try:        
        tokens = lexer.tokenize(input)
        analyzer = syntaxer.SyntaxAnalyzer(tokens)
        syntaxTree = analyzer.parse()
        textTree = analyzer.getTextTree(syntaxTree)
        semanalyzer.SemanticAnalyzer().check(syntaxTree)
        output = codegen.CodeGenerator().genJavaScript(syntaxTree)
    except Exception as err:
        flash(f'{type(err)}: {err}', category='error')

    return render_template('index.html', input=input, output=output, syntaxTree=textTree, tokens='\n'.join(map(str, tokens)))


if __name__ == '__main__':
    app.run(debug=False)
