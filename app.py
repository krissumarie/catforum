import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import psycopg
from flask import Flask, render_template, request, session, flash, redirect
from database.database import create_database
from database.user import create_user, check_user
# muudatus

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'
with app.app_context():
    create_database()

def get_db_connection():
    return psycopg.connect(app.config['POSTGRES_CONNECTION_STRING'])


@app.route('/')
def index():
    if 'username' in session:
        return render_template('enda_konto.html', username=session['username'])
    return render_template('index.html')


@app.route('/profiiliseaded')
def profiiliseaded():
    return render_template('profiiliseaded.html')

@app.route('/enda_konto')
def enda_konto():
    if 'username' not in session:
        flash('You must be logged in to view this page.', 'danger')
        return redirect('/sisselogimine')
    return render_template('enda_konto.html', username=session['username'])

@app.route('/signup', methods=["POST"])
def signup():
    name = request.form.get('name')
    password = request.form.get('password')

    try:
        with psycopg.connect(app.config['POSTGRES_CONNECTION_STRING']) as conn:
            with conn.cursor() as cur:
                # Directly insert the password without hashing
                cur.execute("""
                        INSERT INTO users (name, password)
                        VALUES (%s, %s)
                    """, (name, password))
                conn.commit()
                flash('Account created successfully!', 'success')
    except psycopg.Error as e:
        flash(f'Error saving to database: {e}', 'danger')

    return redirect('/')



@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('name')
    password = request.form.get('password')

    print(f"Attempting to log in with username: {username} and password: {password}")

    try:
        with psycopg.connect(app.config['POSTGRES_CONNECTION_STRING']) as conn:
            with conn.cursor() as cur:
                # Query the database for the user's stored password (in plain text)
                cur.execute("SELECT password FROM users WHERE name = %s", (username,))
                result = cur.fetchone()

                if result:
                    db_password = result[0]
                    print(f"Database password: {db_password}")  # Debug print

                    # Direct comparison of plain text passwords
                    if password == db_password:
                        session['username'] = username
                        flash('Login successful!', 'success')
                        return redirect('/')  # Redirect to the home page
                    else:
                        flash('Invalid credentials', 'danger')
                else:
                    flash('User does not exist', 'danger')

    except psycopg.Error as e:
        flash(f"Database error: {e}", 'danger')

    return render_template('sisselogimine.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user session
    flash('You have been logged out.', 'info')
    return redirect('/')


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