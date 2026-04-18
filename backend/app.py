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

    username = data.get("username")
    password = data.get("password")

    # ROLE BASED LOGIN
    users = {
        "admin": {"password": "1234", "role": "Admin"},
        "manager": {"password": "1234", "role": "Manager"},
        "employee": {"password": "1234", "role": "Employee"}
    }

    user = users.get(username)

    if user and user["password"] == password:
        return jsonify({
            "message": "Login successful",
            "role": user["role"]
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401


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
 # ---------------- ROLE DATA ----------------
roles = [
    {
        "id": 1,
        "name": "Admin",
        "description": "Full access to system",
        "permissions": ["add", "edit", "delete"],
        "department_id": None,
        "status": "active"
    },
    {
        "id": 2,
        "name": "Employee",
        "description": "View only access",
        "permissions": ["view"],
        "department_id": None,
        "status": "active"
    }
]

role_id_counter = 3


# ---------------- ADD ROLE ----------------
@app.route("/add_role", methods=["POST"])
def add_role():
    global role_id_counter

    data = request.json

    role_name = data.get("name")
    role_description = data.get("description")
    permissions = data.get("permissions", [])
    department_id = data.get("department_id")

    if not role_name:
        return jsonify({"error": "Role name required"}), 400

    new_role = {
        "id": role_id_counter,
        "name": role_name,
        "description": role_description,
        "permissions": permissions,
        "department_id": department_id,
        "status": "active"
    }

    roles.append(new_role)
    role_id_counter += 1

    return jsonify({"message": "Role added successfully", "role": new_role})


# ---------------- GET ACTIVE ROLES ----------------
@app.route("/get_roles", methods=["GET"])
def get_roles():
    return jsonify([r for r in roles if r["status"] == "active"])


# ---------------- GET DELETED ROLES ----------------
@app.route("/get_deleted_roles", methods=["GET"])
def get_deleted_roles():
    return jsonify([r for r in roles if r["status"] == "deleted"])


# ---------------- UPDATE ROLE ----------------
@app.route("/update_role/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.json

    for role in roles:
        if role["id"] == role_id:
            role["name"] = data.get("name", role["name"])
            role["description"] = data.get("description", role.get("description"))
            role["permissions"] = data.get("permissions", role["permissions"])
            role["department_id"] = data.get("department_id", role["department_id"])

            return jsonify({"message": "Role updated successfully", "role": role})

    return jsonify({"error": "Role not found"}), 404


# ---------------- DELETE ROLE ----------------
@app.route("/delete_role/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    for role in roles:
        if role["id"] == role_id:
            role["status"] = "deleted"
            return jsonify({"message": "Role deleted successfully"})

    return jsonify({"error": "Role not found"}), 404


# ---------------- RESTORE ROLE ----------------
@app.route("/restore_role/<int:role_id>", methods=["PUT"])
def restore_role(role_id):
    for role in roles:
        if role["id"] == role_id:
            role["status"] = "active"
            return jsonify({"message": "Role restored successfully"})

    return jsonify({"error": "Role not found"}), 404
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)