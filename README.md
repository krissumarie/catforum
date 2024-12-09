
**Kuidas käivatada meie veebilehte:**

1. Kõigepealt lae alla PostgreSQL programm. Seal sul nõutakse luua parool, mida on vaja meeles pidada.

2. Loo pycharmis endale oma config.py file, kasutades config.example.py faili. Seal sisesta ka oma postgresqli parool.

3. Pärast postgresql seadistamist on sul vaja avada pycharmis terminal ja sisestada need commandid ükshaaval:

- py -m venv venv\

- venv/Scripts/activate

- pip install -r requirements.txt

4. Lõpuks paned viimase commandi: flask --debug run ja siis peaks tulema link meie lehele.

5. Lisaks on meil võimalus luua postitusi ja selleks on vaja avada arvutist SQL Shell (psql) terminal, kus paned jälle oma postqre parooli ning sisestad terminali selle:
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,                  -- Unique identifier for each post
    title VARCHAR(2048) NOT NULL,           -- Title of the post
    text TEXT NOT NULL,                    -- Text content of the post
    username VARCHAR(255) NOT NULL,        -- Username of the creator
    image_path VARCHAR(255),               -- Path to the uploaded image file
    created_at TIMESTAMP DEFAULT NOW()     -- Timestamp of post creation
);

6. Enda konto muutmiseks on vaja SQL Shelli (psql) terminali sisestada:
    CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
    user_id INTEGER NOT NULL UNIQUE, -- Unique identifier for the user
    profile_picture TEXT DEFAULT '/path/to/default_image.jpg', -- Default profile picture
    bio1 TEXT DEFAULT '', -- Default empty text for bio1
    bio2 TEXT DEFAULT ''  -- Default empty text for bio2
);


Siis kirjuta \dt et kontrollida, kas su tabelis on 4 rida.
