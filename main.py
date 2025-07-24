from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import sqlite3
import os, json
from datetime import datetime, timedelta

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
                definition TEXT,
                pons TEXT,
                coef INTEGER,
                after TEXT
            )
        ''')
        conn.commit()

def translate(text, lng):
    url = 'https://clients5.google.com/translate_a/t'
    params = {
        'client': 'dict-chrome-ex',
        'sl': 'de',
        'tl': lng,
        'q': text
        }
    hdr = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
    response = requests.get(url, headers=hdr, params=params, proxies=PROXIES)
    if response.ok:
        try:
            return response.json()[0]
        except Exception:
            return ""
    return ""

def translate_PONS(text):
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
            return response.text
        except Exception:
            return ""
    return ""

# Get definition from Google Dictionary API (unofficial, for demo purposes)
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    hdr = {
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }
    response = requests.get(url, proxies=PROXIES)
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
        german = request.form["german"].strip().capitalize()
        english = translate(german, "en").capitalize()
        persian = translate(german, "fa").capitalize()
        definition = get_definition(english)
        pons = translate_PONS(german)
        if persian == english:
            return redirect(url_for("index"))        
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO flashcards (german, english, persian, definition, pons, coef, after) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (german, english, persian, definition, pons, 1, str(datetime.today())))
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
        #WHERE after>='{str(datetime.today())}'
        c.execute(f"SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1")
        card = c.fetchone()
        if card is None:
            c.execute(f"SELECT * FROM flashcards WHERE id=0")
            card = c.fetchone()
    return render_template("practice.html",
                           card={
                               'id':card[0],
                               'de':card[1],
                               'en':card[2],
                               'fa':card[3],
                               'tx':card[4]},
                           pons=json.loads(card[5]))

@app.route("/knew/<int:card_id>")
def knew(card_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(f"SELECT coef FROM flashcards WHERE id={card_id}")
        coef = c.fetchone()[0]
        after = str(datetime.today()+timedelta(days=coef))
        coef=(2*coef)%17
        c.execute(f"UPDATE flashcards SET coef={coef}, after='{after}' WHERE id={card_id}")
    return redirect(url_for('practice'))
    
@app.route("/forgot/<int:card_id>")
def forgot(card_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        after = str(datetime.today())
        c.execute(f"UPDATE flashcards SET coef=1, after='{after}' WHERE id={card_id}")
    return redirect(url_for('practice'))


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)







'''
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
''' 
    
    
    
    
    
