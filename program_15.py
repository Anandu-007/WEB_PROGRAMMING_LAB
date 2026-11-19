
from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_secret_key"

# Common CSS
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
        width: 320px;
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

    a {
        display: inline-block;
        margin-top: 15px;
    }

    p {
        color: red;
    }
</style>
"""

# Create database
def create_table():
    con = sqlite3.connect("users.db")

    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    con.commit()
    con.close()

# Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    msg = ""

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or len(password) < 8:
            msg = "Username required and password must be 8 characters!"
        else:
            con = sqlite3.connect("users.db")

            try:
                hashed = generate_password_hash(password)

                con.execute(
                    "INSERT INTO users(username,password) VALUES(?,?)",
                    (username, hashed)
                )

                con.commit()
                msg = "Registration successful!"

            except sqlite3.IntegrityError:
                msg = "Username already exists!"

            con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">
            <h2>Register</h2>

            <form method="POST">
                <input name="username" placeholder="Username" required>

                <input name="password" type="password"
                       placeholder="Password" required>

                <button type="submit">Register</button>
            </form>

            <p>{{msg}}</p>
            <a href="/login">Login</a>
        </div>
    """, msg=msg)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    msg = ""

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        con = sqlite3.connect("users.db")

        user = con.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        con.close()

        if user and check_password_hash(user[2], password):
            session["username"] = username
            return redirect("/dashboard")
        else:
            msg = "Invalid username or password!"

    return render_template_string("""
        """ + style + """
        <div class="container">
            <h2>Login</h2>

            <form method="POST">
                <input name="username" placeholder="Username" required>

                <input name="password" type="password"
                       placeholder="Password" required>

                <button type="submit">Login</button>
            </form>

            <p>{{msg}}</p>
            <a href="/register">Register</a>
        </div>
    """, msg=msg)

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "username" in session:
        return render_template_string("""
            <h2>Welcome {{name}}</h2>
            <a href="/logout">Logout</a>
        """, name=session["username"])

    return redirect("/login")

# Logout
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
