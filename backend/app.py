from flask import Flask, request, jsonify
from db import db, cursor

app = Flask(__name__)

@app.route("/")
def home():
    return "HRM Backend Running"


# Add Department API
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


# View Departments API
@app.route("/departments", methods=["GET"])
def get_departments():

    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()

    result = []

    for dept in departments:
        result.append({
            "dept_id": dept[0],
            "dept_name": dept[1],
            "description": dept[2],
            "created_at": str(dept[3]),
            "updated_at": str(dept[4]),
            "status": dept[5]
        })

    return jsonify(result)
@app.route("/update_department/<int:id>", methods=["PUT"])
def update_department(id):

    data = request.json

    dept_name = data["dept_name"]
    description = data["description"]

    query = "UPDATE department SET dept_name=%s, description=%s WHERE dept_id=%s"
    values = (dept_name, description, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Department updated successfully"})


if __name__ == "__main__":
    app.run(debug=True)