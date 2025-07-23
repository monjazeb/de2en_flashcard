from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import sqlite3
import os

APIKEY = 'AIzaSyCBv1iqQ41ufsP7bbnxKbIYFCOqrMiEsfM'
SECRET = '1e049a9c1e4d2dddf763e62c18d44081ecea61041b5d1e8529604c1a3076be37'
BASEURL = 'https://api.pons.com/v1/dictionary'

PROXIES = {'http': 'http://sophosutm.mevis.lokal:8080',
           'https': 'http://sophosutm.mevis.lokal:8080'}
app = Flask(__name__)

DB_PATH = "flashcards.db"

# Initialize database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                german TEXT NOT NULL,
                english TEXT,
                persian TEXT,
                definition TEXT
            )
        ''')
        conn.commit()

# Google Translate API (unofficial, for demo purposes)
def translate(text):
          #https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=de&tl=fa&q=wort
    url = BASEURL
    params = {
        "l": "deen",
        "q": text
        }
    hdr = {'X-Secret': SECRET,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
    response = requests.get(url, headers=hdr, params=params, proxies=PROXIES)
    if response.ok:
        try:
            return response.json()
        except Exception:
            return ""
    return ""

# Get definition from Google Dictionary API (unofficial, for demo purposes)
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.ok:
        try:
            data = response.json()
            return data[0]["meanings"][0]["definitions"][0]["definition"]
        except Exception:
            return ""
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        german = request.form["german"].strip()
        english = translate(german, "en")
        persian = translate(german, "fa")
        definition = get_definition(english)
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO flashcards (german, english, persian, definition) VALUES (?, ?, ?, ?)",
                      (german, english, persian, definition))
            conn.commit()
        return redirect(url_for("index"))
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flashcards")
        flashcards = c.fetchall()
    return render_template("index.html", flashcards=flashcards)

@app.route("/practice")
def practice():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1")
        card = c.fetchone()
    return render_template("practice.html", card=card)

@app.route("/reveal/<int:card_id>")
def reveal(card_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flashcards WHERE id=?", (card_id,))
        card = c.fetchone()
    return jsonify({
        "english": card[2],
        "persian": card[3],
        "definition": card[4]
    })

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    for a in translate('fast'):
        print(a['lang'])
        for b in a['hits']:
            #print(b['type'])
            print('-----------')
            for c in b['roms']:
                #print(c['headword'], end='->')
                #print(c['headword_full'], end='->')
                #print(c['wordclass'], end='->')
                for d in c['arabs']:
                    #print(d['header'])
                    for e in d['translations']:
                        print(e['target'])
                    continue
    #['hits'][0]['roms'][0]['arabs']:
    
    
    
    
    
    
#    app.run(debug=True)
