import sqlite3
from datetime import datetime
from flask import Flask, render_template, request
import pickle
import string

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    return text

def init_db():
    conn = sqlite3.connect("history.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            prediction TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

SCAM_KEYWORDS = [
    "win", "won", "winner", "prize", "lottery", "claim",
    "click here", "click now", "urgent", "free money",
    "account blocked", "verify account", "bank update",
    "limited offer", "congratulations", "gift card",
    "cash reward", "claim now", "otp", "password", "login"
]

SAFE_CASUAL = [
    "hi", "hello", "hey", "how are you", "come soon",
    "call me", "meet tomorrow", "where are you",
    "i am", "bro", "rohan", "manmeet", "okay", "ok"
]

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        message = request.form["message"]
        message_clean = clean_text(message)

        if any(keyword in message_clean for keyword in SCAM_KEYWORDS):
            result = "🚨 SCAM/SPAM (rule-based keyword detection)"

        elif any(phrase in message_clean for phrase in SAFE_CASUAL):
            result = "✅ SAFE (casual conversation detected)"

        elif len(message_clean.split()) <= 4:
            result = "✅ SAFE (short casual message)"

        else:
            data = vectorizer.transform([message_clean])
            spam_prob = model.predict_proba(data)[0][1]

            if spam_prob >= 0.85:
                result = f"🚨 SCAM/SPAM (confidence: {spam_prob*100:.1f}%)"
            else:
                result = f"✅ SAFE (confidence: {(1-spam_prob)*100:.1f}%)"

        conn = sqlite3.connect("history.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO logs (ts, prediction, message) VALUES (?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result, message[:200])
        )
        conn.commit()
        conn.close()

    conn = sqlite3.connect("history.db")
    cur = conn.cursor()
    cur.execute("SELECT ts, prediction, message FROM logs ORDER BY id DESC LIMIT 10")
    history = cur.fetchall()
    conn.close()

    return render_template("index.html", result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)
