import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import psycopg
from flask import Flask, render_template, request, session, flash, redirect
from database.database import create_database
from werkzeug.utils import secure_filename
from flask import send_from_directory


app = Flask(__name__, static_folder='static')
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'
app.config['SECRET_KEY'] = 'your_secret_key'
with app.app_context():
    create_database()

def get_db_connection():
    return psycopg.connect(app.config['POSTGRES_CONNECTION_STRING'])


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
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

UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/postituseloomine', methods=["GET", "POST"])
def postituseloomine():
    # Check if the user is logged in
    if 'username' not in session:
        flash('You must be logged in to create a post.', 'danger')
        return redirect('/sisselogimiSne')

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        text = request.form.get('text')
        file = request.files.get('image')

        # Validate form inputs
        if not title:
            flash('Title is required.', 'danger')
            return redirect('/postituseloomine')
        if not text:
            flash('Text is required.', 'danger')
            return redirect('/postituseloomine')
        if not file or not allowed_file(file.filename):
            flash('A valid image file is required.', 'danger')
            return redirect('/postituseloomine')

        # Handle file upload
        image_path = None
        if file:
            filename = secure_filename(file.filename)
            flash('File added!', 'success')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"uploads/{filename}"  # Store the relative path

        try:
            # Save the post to the database
            with psycopg.connect(app.config['POSTGRES_CONNECTION_STRING']) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO posts (title, text, username, image_path)
                        VALUES (%s, %s, %s, %s)
                    """, (title, text, session['username'], image_path))
                    conn.commit()
                    flash('Post created successfully!', 'success')
                    return redirect('/')  # Redirect to the home page after posting
        except psycopg.Error as e:
            flash(f'Error saving post to the database: {e}', 'danger')

    # Render the post creation form
    return render_template('postituseloomine.html')




@app.route('/uploads')
def uploads():
    posts = []
    try:
        with psycopg.connect(app.config['POSTGRES_CONNECTION_STRING']) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT title, text, image_path, username FROM posts ORDER BY id DESC
                """)
                posts = cur.fetchall()
                print(f"Posts fetched: {posts}")  # Debug print to check data
    except psycopg.Error as e:
        flash(f"Database error: {e}", 'danger')

    # Normalize the image path to use forward slashes (ensure consistency)
    posts = [{
        'headline': post[0],
        'text': post[1],
        'image_path': post[2].replace('\\', '/'),  # Make sure to replace backslashes with forward slashes
        'username': post[3]
    } for post in posts]

    return render_template('uploads.html', posts=posts)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.secret_key = 'your_secret_key'

if __name__ == '__main__':
    app.run()