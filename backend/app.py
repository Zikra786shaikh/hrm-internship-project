from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ TEMP STORAGE (acts like database)
departments = [
    {"dept_id": 1, "dept_name": "HR", "description": "Human Resource", "status": 1},
    {"dept_id": 2, "dept_name": "IT", "description": "Tech", "status": 1}
]

next_id = 3


@app.route("/")
def home():
    return "Backend Running"


# ---------------- LOGIN ----------------
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json

    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# ---------------- GET ACTIVE ----------------
@app.route("/departments", methods=["GET"])
def get_departments():
    return jsonify([d for d in departments if d["status"] == 1])


# ---------------- ADD ----------------
@app.route("/add_department", methods=["POST"])
def add_department():
    global next_id

    data = request.json

    new_dept = {
        "dept_id": next_id,
        "dept_name": data.get("dept_name"),
        "description": data.get("description"),
        "status": 1
    }

    departments.append(new_dept)
    next_id += 1

    return jsonify({"message": "Department added"})


# ---------------- DELETE (SOFT) ----------------
@app.route("/delete_department/<int:id>", methods=["DELETE"])
def delete_department(id):
    for d in departments:
        if d["dept_id"] == id:
            d["status"] = 0
            return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404


# ---------------- UPDATE ----------------
@app.route("/update_department/<int:id>", methods=["PUT"])
def update_department(id):
    data = request.json

    for d in departments:
        if d["dept_id"] == id:
            d["dept_name"] = data.get("dept_name")
            d["description"] = data.get("description")
            return jsonify({"message": "Updated"})

    return jsonify({"message": "Not found"}), 404


# ---------------- DELETED ----------------
@app.route("/deleted_departments", methods=["GET"])
def deleted_departments():
    return jsonify([d for d in departments if d["status"] == 0])


# ---------------- RESTORE ----------------
@app.route("/restore_department/<int:id>", methods=["PUT"])
def restore_department(id):
    for d in departments:
        if d["dept_id"] == id:
            d["status"] = 1
            return jsonify({"message": "Restored"})
    return jsonify({"message": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)