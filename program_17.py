
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

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
        padding: 20px 0;
    }

    .container {
        background-color: white;
        padding: 30px;
        width: 500px;
        max-width: 90%;
        border-radius: 10px;
        box-shadow: 0 0 10px gray;
        text-align: center;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
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
        padding: 12px;
        margin: 10px 0;
        border-radius: 5px;
        overflow-wrap: anywhere;
    }

    a {
        color: #007bff;
        text-decoration: none;
        margin: 5px;
    }
</style>
"""

# Database connection
def connect():
    return sqlite3.connect("employee.db")

# Create table
def create_table():

    con = connect()

    con.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary REAL
        )
    """)

    con.commit()
    con.close()

# Home page - Add and display employees
@app.route("/", methods=["GET", "POST"])
def index():

    con = connect()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]

        con.execute(
            "INSERT INTO employees(name,department,salary) VALUES(?,?,?)",
            (name, department, salary)
        )

        con.commit()

    employees = con.execute(
        "SELECT * FROM employees"
    ).fetchall()

    con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">

            <h2>Employee Management System</h2>

            <h3>Add Employee</h3>

            <form method="POST">
                <input name="name" placeholder="Employee Name" required>

                <input name="department" placeholder="Department" required>

                <input name="salary" type="number"
                       step="0.01" placeholder="Salary" required>

                <button type="submit">Add Employee</button>
            </form>

            <h3>Search Employee</h3>

            <form action="/search" method="GET">
                <input name="keyword" placeholder="Enter name or ID">
                <button type="submit">Search</button>
            </form>

            <h3>Employee Records</h3>

            {% for e in employees %}
                <div class="record">
                    <p>
                        ID: {{e[0]}}<br>
                        Name: {{e[1]}}<br>
                        Department: {{e[2]}}<br>
                        Salary: {{e[3]}}
                    </p>

                    <a href="/edit/{{e[0]}}">Edit</a>
                    <a href="/delete/{{e[0]}}">Delete</a>
                </div>
            {% endfor %}

        </div>
    """, employees=employees)

# Search employee
@app.route("/search")
def search():

    keyword = request.args.get("keyword", "").strip()

    con = connect()

    employees = con.execute("""
        SELECT * FROM employees
        WHERE name LIKE ? OR CAST(id AS TEXT) = ?
    """, ("%" + keyword + "%", keyword)).fetchall()

    con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">

            <h2>Search Results</h2>

            {% for e in employees %}
                <div class="record">
                    <p>
                        ID: {{e[0]}}<br>
                        Name: {{e[1]}}<br>
                        Department: {{e[2]}}<br>
                        Salary: {{e[3]}}
                    </p>
                </div>
            {% else %}
                <p>No employees found</p>
            {% endfor %}

            <a href="/">Back</a>

        </div>
    """, employees=employees)

# Update employee
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    con = connect()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]

        con.execute("""
            UPDATE employees
            SET name=?, department=?, salary=?
            WHERE id=?
        """, (name, department, salary, id))

        con.commit()
        con.close()

        return redirect("/")

    employee = con.execute(
        "SELECT * FROM employees WHERE id=?", (id,)
    ).fetchone()

    con.close()

    return render_template_string("""
        """ + style + """
        <div class="container">

            <h2>Update Employee</h2>

            <form method="POST">
                <input name="name" value="{{e[1]}}" required>

                <input name="department" value="{{e[2]}}" required>

                <input name="salary" type="number" step="0.01"
                       value="{{e[3]}}" required>

                <button type="submit">Update</button>
            </form>

            <a href="/">Back</a>

        </div>
    """, e=employee)

# Delete employee
@app.route("/delete/<int:id>")
def delete(id):

    con = connect()

    con.execute("DELETE FROM employees WHERE id=?", (id,))

    con.commit()
    con.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
