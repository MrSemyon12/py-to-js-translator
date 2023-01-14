from flask import Flask, render_template, request, flash
import lexer
import syntaxer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadawedij3u47r3476666%$^&788782390(())*^$@@@fsfd'


@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')
    output = ''
    operationTree = ''
    syntaxTree = ''

    if not input:
        return render_template('index.html', input='', output=output, operationTree=operationTree, syntaxTree=syntaxTree)

    try:
        tokens = list(lexer.tokenize(input))
        analyzer = syntaxer.SyntaxAnalyzer(tokens)
        tree = analyzer.parse()
        syntaxTree = analyzer.getTree(tree)
        output = 'aaa'
    except Exception as err:
        flash(f'{type(err)}: {err}', category='error')

    return render_template('index.html', input=input, output=output, operationTree=operationTree, syntaxTree=syntaxTree)


if __name__ == '__main__':
    app.run(debug=True)
