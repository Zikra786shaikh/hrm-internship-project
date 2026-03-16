from flask import Flask, request, jsonify
from db import db, cursor

app = Flask(__name__)

@app.route("/")
def home():
    return "HRM Backend Running"


@app.route("/add_department", methods=["POST"])
def add_department():
    data = request.json

    dept_name = data["dept_name"]
    description = data["description"]

    query = "INSERT INTO department (dept_name, description) VALUES (%s, %s)"
    values = (dept_name, description)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Department added successfully"})


if __name__ == "__main__":
    app.run(debug=True)