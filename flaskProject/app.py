from flask import Flask
from flask import render_template
from flask import request
from flaskProject.database.database import create_database
from flask import session, flash
from flask import Flask, redirect

from flaskProject.database.user import create_user

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

# app.config.from_object('config:Config')
with app.app_context(): # must be in application context to execute
    create_database()


@app.route('/signup', methods=["POST"])
def signup():
    name = request.form.get('name')
    password = request.form.get('password')
    create_user(name, password)
    return redirect("/")

@app.route('/sisselogimine')
def sisselogimine():
    return render_template('sisselogimine.html')

@app.route('/registreerimine')
def registreerimine():
    return render_template('registreerimine.html')


if __name__ == '__main__':
    app.run()