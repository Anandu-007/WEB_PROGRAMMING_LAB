
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# CSS Styling
style = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
    }

    .container {
        background-color: white;
        padding: 30px;
        width: 400px;
        border-radius: 10px;
        box-shadow: 0 0 10px gray;
        text-align: center;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        box-sizing: border-box;
    }

    button {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    .record {
        background-color: #f2f2f2;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }

    a {
        margin: 5px;
        color: #007bff;
        text-decoration: none;
    }
</style>
"""

# Database connection
def connect():
    return sqlite3.connect("students.db")

# Create table
def create_table():
    con = connect()

    con.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)

    con.commit()
    con.close()

# Display records and add new record
@app.route("/", methods=["GET", "POST"])
def index():

    con = connect()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        con.execute(
            "INSERT INTO students(name,email) VALUES(?,?)",
            (name, email)
        )

        con.commit()

    records = con.execute("SELECT * FROM students").fetchall()
    con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">

            <h2>Student Management</h2>

            <form method="POST">
                <input name="name" placeholder="Name" required>

                <input name="email" type="email"
                       placeholder="Email" required>

                <button type="submit">Add Student</button>
            </form>

            <h3>Student Records</h3>

            {% for r in records %}
                <div class="record">
                    <p>{{r[1]}} - {{r[2]}}</p>

                    <a href="/edit/{{r[0]}}">Edit</a>

                    <a href="/delete/{{r[0]}}">Delete</a>
                </div>
            {% endfor %}

        </div>
    """, records=records)

# Update record
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    con = connect()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        con.execute(
            "UPDATE students SET name=?,email=? WHERE id=?",
            (name, email, id)
        )

        con.commit()
        con.close()

        return redirect("/")

    record = con.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">

            <h2>Edit Student</h2>

            <form method="POST">
                <input name="name" value="{{r[1]}}" required>

                <input name="email" type="email"
                       value="{{r[2]}}" required>

                <button type="submit">Update</button>
            </form>

            <a href="/">Back</a>

        </div>
    """, r=record)

# Delete record
@app.route("/delete/<int:id>")
def delete(id):

    con = connect()

    con.execute("DELETE FROM students WHERE id=?", (id,))

    con.commit()
    con.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
