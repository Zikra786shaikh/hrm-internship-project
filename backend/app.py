from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db, cursor

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "HRM Backend Running"


# ---------------- LOGIN ----------------
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    cursor.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ---------------- ADD ----------------
@app.route("/add_department", methods=["POST"])
def add_department():
    data = request.json

    dept_name = data.get("dept_name")
    description = data.get("description")

    cursor.execute(
        "INSERT INTO department (dept_name, description, status) VALUES (%s,%s,1)",
        (dept_name, description)
    )
    db.commit()

    return jsonify({"message": "Added"})


# ---------------- ACTIVE ----------------
@app.route("/departments", methods=["GET"])
def get_departments():
    cursor.execute("SELECT * FROM department WHERE status=1")
    data = cursor.fetchall()

    result = []
    for d in data:
        result.append({
            "dept_id": d[0],
            "dept_name": d[1],
            "description": d[2]
        })

    return jsonify(result)


# ---------------- DELETE ----------------
@app.route("/delete_department/<int:id>", methods=["DELETE"])
def delete_department(id):

    cursor.execute("UPDATE department SET status=0 WHERE dept_id=%s", (id,))
    db.commit()

    print("Deleted ID:", id)  # debug

    return jsonify({"message": "Deleted"})

#--------------update--------------
@app.route("/update_department/<int:id>", methods=["PUT"])
def update_department(id):

    data = request.json

    dept_name = data.get("dept_name")
    description = data.get("description")

    cursor.execute(
        "UPDATE department SET dept_name=%s, description=%s WHERE dept_id=%s",
        (dept_name, description, id)
    )
    db.commit()

    return jsonify({"message": "Updated successfully"})

# ---------------- RESTORE ----------------
@app.route("/restore_department/<int:id>", methods=["PUT"])
def restore_department(id):

    cursor.execute("UPDATE department SET status=1 WHERE dept_id=%s", (id,))
    db.commit()

    return jsonify({"message": "Restored"})


# ---------------- DELETED ----------------
@app.route("/deleted_departments", methods=["GET"])
def deleted_departments():

    cursor.execute("SELECT * FROM department WHERE status=0")
    data = cursor.fetchall()

    print("Deleted Data:", data)  # debug

    result = []

    for d in data:
        result.append({
            "dept_id": d[0],
            "dept_name": d[1],
            "description": d[2]
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)