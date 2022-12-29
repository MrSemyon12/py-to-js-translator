from flask import Flask, render_template, request, flash
from translator.main import test
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadawedij3u47r3476666%$^&788782390(())*^$@@@fsfd'

basedir = path.abspath(path.dirname(__file__))


@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')

    if not input:
        return render_template('index.html', input='', output='')

    print(input)
    with open(r'code/translator/input.txt', 'w') as file:
        file.write(input)

    try:
        test(path.join(basedir, 'translator/'))
        with open(r'code/translator/output.txt', 'r') as file:
            output = file.read()
    except Exception as err:
        flash(f"Unexpected {err}, {type(err)}", category='error')
        output = ''

    return render_template('index.html', input=input, output=output)


if __name__ == '__main__':
    app.run(debug=True)
