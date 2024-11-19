
**Kuidas käivatada meie veebilehte:**

1. Kõigepealt lae alla PostgreSQL programm. Seal sul nõutakse luua parool, mida on vaja meeles pidada.

2. Loo pycharmis endale oma config.py file, kasutades config.example.py faili. Seal sisesta ka oma postgresqli parool.

3. Pärast postgresql seadistamist on sul vaja avada pycharmis terminal ja sisestada need commandid ükshaaval:

- py -m venv venv\

- venv/Scripts/activate

-pip install -r requirements.txt

4. Lõpuks paned viimase commandi: flask --debug run ja siis peaks tulema link meie lehele.
