from flask import Flask, render_template, request, flash
from translator.main import test
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadawedij3u47r3476666%$^&788782390(())*^$@@@fsfd'

basedir = path.abspath(path.dirname(__file__))


@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')
    output = ''
    operationTree = ''
    syntaxTree = ''

    if not input:
        return render_template('index.html', input='', output=output, operationTree=operationTree, syntaxTree=syntaxTree)

    with open('code/translator/input.txt', 'w') as file:
        file.write(input)

    try:
        test(path.join(basedir, 'translator/'))
        with open('code/translator/output.txt', 'r') as file:
            output = file.read()
        with open('code/translator/outputOperationTree.txt', 'r') as file:
            operationTree = file.read()
        with open('code/translator/outputSyntaxTree.txt', 'r') as file:
            syntaxTree = file.read()
    except Exception as err:
        flash(f"{err}", category='error')

    return render_template('index.html', input=input, output=output, operationTree=operationTree, syntaxTree=syntaxTree)


if __name__ == '__main__':
    app.run(debug=False)
