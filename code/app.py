from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    input = request.args.get('input')
    with open(r'code/translator/output.txt', 'r') as file:
        output = file.read()
    print(output)
    return render_template('index.html', input=input, output=output)


if __name__ == '__main__':
    app.run(debug=True)
