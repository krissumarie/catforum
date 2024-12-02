import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import psycopg
from flask import Flask, render_template, request, session, flash, redirect, url_for
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
                # Query the database for the user's stored password and ID
                cur.execute("SELECT id, password FROM users WHERE name = %s", (username,))
                result = cur.fetchone()

                if result:
                    user_id, db_password = result
                    print(f"Database password: {db_password}")  # Debug print

                    # Direct comparison of plain-text passwords
                    if password == db_password:
                        session['user_id'] = user_id
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


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

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
        return redirect('/sisselogimine')

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




@app.route('/')
def index():
    posts = []
    try:
        with psycopg.connect(app.config['POSTGRES_CONNECTION_STRING']) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT title, text, image_path, username FROM posts ORDER BY id DESC
                """)
                posts = cur.fetchall()
                print(f"Posts fetched from DB: {posts}")  # Debug print to check raw data
    except psycopg.Error as e:
        flash(f"Database error: {e}", 'danger')
        print(f"Database error: {e}")  # Additional logging for debugging

    # Check if data exists
    if not posts:
        print("No posts retrieved from the database.")

    # Normalize the data structure for template usage
    posts = [{
        'headline': post[0],
        'text': post[1],
        'image_path': post[2].replace('\\', '/') if post[2] else None,  # Ensure None is handled
        'username': post[3]
    } for post in posts]

    print(f"Posts prepared for template: {posts}")  # Debug transformed data
    return render_template('index.html', posts=posts)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.secret_key = "your_secret_key"

# Database and upload folder setup
UPLOAD_FOLDER2 = os.path.join(app.root_path, 'static', 'profile_pictures')
os.makedirs(UPLOAD_FOLDER2, exist_ok=True)  # Ensure the upload folder exists
conn = psycopg.connect(app.config['POSTGRES_CONNECTION_STRING'])
cursor = conn.cursor()

# Utility: Fetch user profile data
def get_user_profile(user_id):
    cursor.execute("""
        SELECT profile_picture, bio1, bio2
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))
    user = cursor.fetchone()
    profile_picture = user[0] if user and user[0] else "/static/profile_pictures/default.jpg"
    bio1 = user[1] if user else ""
    bio2 = user[2] if user else ""
    return profile_picture, bio1, bio2


@app.route('/enda_konto')
def enda_konto():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to view this page.", "danger")
        return redirect('/sisselogimine')

    profile_picture, bio1, bio2 = get_user_profile(user_id)
    return render_template('enda_konto.html', profile_picture=profile_picture, bio1=bio1, bio2=bio2)


@app.route('/profiiliseaded', methods=['GET', 'POST'])
def profiiliseaded():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to update your profile.", "danger")
        return redirect('/sisselogimine')

    if request.method == 'POST':
        bio1 = request.form.get('bio1', '')
        bio2 = request.form.get('bio2', '')
        file = request.files.get('profile_picture')

        # Handle profile picture upload
        profile_picture_url = None
        if file and file.filename:
            filename = secure_filename(f"user_{user_id}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER2, filename)
            file.save(file_path)
            profile_picture_url = f"static/profile_pictures/{filename}"

        # Insert or update profile in the database
        try:
            cursor.execute("SELECT 1 FROM user_profiles WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                if profile_picture_url:
                    cursor.execute("""
                        UPDATE user_profiles
                        SET profile_picture = %s, bio1 = %s, bio2 = %s
                        WHERE user_id = %s
                    """, (profile_picture_url, bio1, bio2, user_id))
                else:
                    cursor.execute("""
                        UPDATE user_profiles
                        SET bio1 = %s, bio2 = %s
                        WHERE user_id = %s
                    """, (bio1, bio2, user_id))
            else:
                cursor.execute("""
                    INSERT INTO user_profiles (user_id, profile_picture, bio1, bio2)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, profile_picture_url or "/static/profile_pictures/default.jpg", bio1, bio2))
            conn.commit()
        except Exception as e:
            flash(f"Error updating profile: {e}", "danger")
            return redirect(url_for('profiiliseaded'))

        flash("Profile updated successfully!", "success")
        return redirect(url_for('enda_konto'))

    profile_picture, bio1, bio2 = get_user_profile(user_id)
    return render_template('profiiliseaded.html', profile_picture=profile_picture, bio1=bio1, bio2=bio2)


if __name__ == '__main__':
    app.run(debug=True)