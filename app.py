from flask import Flask, request, render_template
import sqlite3

# Initialize the Flask app
app = Flask(__name__)

# Function to connect to the database
def get_db_connect():
    conn = sqlite3.connect("mydatabase.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
def init_db():
    conn = get_db_connect()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Route for form
@app.route('/')
def form():
    return render_template('form.html')

# Route to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']

    conn = get_db_connect()
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

    return "User added successfully by Nabiswa James <a href='/'>Add Another</a>"

# Route to list all users
@app.route('/users')
def list_users():
    conn = get_db_connect()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    html = "<h2>ALL USERS</h2><table border='1'><tr><th>ID</th><th>Name</th><th>Age</th></tr>"
    for row in rows:
        html += f"<tr><td>{row['id']}</td><td>{row['name']}</td><td>{row['age']}</td></tr>"
    html += "</table><br><a href='/'>Back to Form</a>"

    return html

# Run the app
if __name__ == '__main__':
    app.run(debug=True)