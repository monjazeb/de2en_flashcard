from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import sqlite3
import os

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
def translate(text, target_lang):
          #https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=de&tl=fa&q=wort
    url = "https://clients5.google.com/translate_a/t"
    params = {
        "client": "dict-chrome-ex",
        "sl": "de",
        "tl": target_lang,
        "dt": "t",
        "q": text
    }
    response = requests.get(url, params=params)
    print(response.text)
    if response.ok:
        try:
            return response.json()[0][0][0]
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
    app.run(debug=True)