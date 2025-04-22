
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# Создание базы данных
def init_db():
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    with open("vpn2.html", "r") as f:
        html = f.read()
    return render_template_string(html)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO subscriptions (email) VALUES (?)', (email,))
        conn.commit()
        message = "Subscribed successfully!"
    except sqlite3.IntegrityError:
        message = "You are already subscribed."
    conn.close()
    return f"<h2>{message}</h2><a href='/'>Go back</a>"

@app.route('/subscribers')
def show_subscribers():
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    c.execute('SELECT email FROM subscriptions')
    emails = c.fetchall()
    conn.close()
    return "<h2>Subscribers List:</h2><ul>" + "".join(f"<li>{email[0]}</li>" for email in emails) + "</ul>"

if __name__ == '__main__':
    app.run(debug=True)
