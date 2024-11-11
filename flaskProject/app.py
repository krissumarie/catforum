from flask import Flask
from flask import render_template
from flask import request
from flaskProject.database.database import create_database
from flask import session, flash
from flask import Flask, redirect
from flaskProject.database.user import create_user, check_user



# muudatus
app = Flask(__name__)
app.secret_key = 'your_secret_key'
with app.app_context():
    create_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profiiliseaded')
def profiiliseaded():
    return render_template('profiiliseaded.html')

@app.route('/enda_konto')
def enda_konto():
    return render_template('enda_konto.html')

@app.route('/signup', methods=["POST"])
def signup():
    name = request.form.get('name')
    password = request.form.get('password')
    create_user(name, password)
    user_id = check_user(name, password)
    if user_id:
        session['user_id'] = user_id
        session['username'] = name
        flash("User created")
        return redirect("/")
    flash("Couldn't create user")
    return redirect("/")


@app.route('/login', methods=["POST"])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user_id = check_user(name, password)
    if user_id:
        session['user_id'] = user_id
        session['username'] = name
        flash("Login successful")
        return redirect("/")
    flash('Invalid credentials')
    return redirect("/")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out')
    return redirect("/")


@app.route('/history')
def history():
    # Your code here
    pass

@app.route('/sisselogimine')
def sisselogimine():
    return render_template('sisselogimine.html')

@app.route('/registreerimine')
def registreerimine():
    return render_template('registreerimine.html')

@app.route('/postitus')
def postitus():
    return render_template('postitus.html')


app.secret_key = 'your_secret_key'

if __name__ == '__main__':
    app.run()