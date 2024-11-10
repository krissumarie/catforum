from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profiiliseaded')
def profiiliseaded():
    return render_template('profiiliseaded.html')

@app.route('/enda_konto')
def enda_konto():
    return render_template('enda_konto.html')

@app.route('/sisselogimine')
def sisselogimine():
    return render_template('sisselogimine.html')

@app.route('/registreerimine')
def registreerimine():
    return render_template('registreerimine.html')


if __name__ == '__main__':
    app.run()