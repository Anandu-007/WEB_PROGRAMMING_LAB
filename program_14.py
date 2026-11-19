
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Create database
def create_table():
    con = sqlite3.connect("contact.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    con.commit()
    con.close()

# HTML form

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Form</title>

    <style>
        body {
            font-family: Arial;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            background: white;
            padding: 30px;
            width: 350px;
            border-radius: 10px;
            box-shadow: 0 2px 10px gray;
        }

        h2 {
            text-align: center;
        }

        input, textarea {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }

        textarea {
            height: 100px;
        }

        button {
            width: 100%;
            padding: 10px;
            background-color: blue;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: darkblue;
        }

        p {
            text-align: center;
            color: green;
        }
    </style>
</head>

<body>

    <div class="container">

        <h2>Contact Form</h2>

        <form method="POST">

            Name:
            <input type="text" name="name" required>

            Email:
            <input type="email" name="email" required>

            Message:
            <textarea name="message" required></textarea>

            <button type="submit">Submit</button>

        </form>

        <p>{{ msg }}</p>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def contact():

    msg = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        con = sqlite3.connect("contact.db")

        con.execute(
            "INSERT INTO contacts(name,email,message) VALUES(?,?,?)",
            (name, email, message)
        )

        con.commit()
        con.close()

        msg = "Contact submitted successfully!"

    return render_template_string(html, msg=msg)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
