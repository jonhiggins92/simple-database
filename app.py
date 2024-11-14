from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# SQLite database setup
DATABASE = 'example.db'

# Function to connect to SQLite
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Initialize the database
def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS records (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT
                        )''')

# Route to display all records
@app.route('/')
def index():
    with get_db() as conn:
        records = conn.execute('SELECT * FROM records').fetchall()
    return render_template('index.html', records=records)

# Route to add a new record
@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    description = request.form['description']
    with get_db() as conn:
        conn.execute('INSERT INTO records (name, description) VALUES (?, ?)', (name, description))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
