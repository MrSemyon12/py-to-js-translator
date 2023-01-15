from flask import Flask, render_template, request, flash
import lexer
import syntaxer
import semanalyzer
import codegen

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smA8691BVVd2bq9iSzeAm2yW1GJJD0dE'


@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')
    output = ''
    textTree = ''

    if not input:
        return render_template('index.html', input='', output=output, syntaxTree=textTree)

    try:
        tokens = list(lexer.tokenize(input))
        analyzer = syntaxer.SyntaxAnalyzer(tokens)
        syntaxTree = analyzer.parse()
        textTree = analyzer.getTextTree(syntaxTree)
        semanalyzer.SemanticAnalyzer().check(syntaxTree)
        output = codegen.CodeGenerator().genJavaScript(syntaxTree)
    except Exception as err:
        flash(f'{type(err)}: {err}', category='error')

    return render_template('index.html', input=input, output=output, syntaxTree=textTree)


if __name__ == '__main__':
    app.run(debug=True)
