from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================== OTP STORAGE ==================
otp_storage = {}

# ================== DEPARTMENT DATA ==================
departments = [
    {"dept_id": 1, "dept_name": "HR", "description": "Human Resource", "status": 1},
    {"dept_id": 2, "dept_name": "IT", "description": "Tech", "status": 1}
]

next_id = 3


@app.route("/")
def home():
    return "Backend Running"


# ================== LOGIN (FIXED WITH EMPLOYEES) ==================
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    for emp in employees:
        if emp["username"] == username and emp["password"] == password:
            
            # role mapping
            role = "Admin" if emp["role_id"] == 1 else "Manager" if emp["role_id"] == 2 else "Employee"

            return jsonify({
                "message": "Login successful",
                "role": role
            })

    return jsonify({"message": "Invalid credentials"}), 401


# ================== FORGOT PASSWORD ==================
@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    for emp in employees:
        if emp["email"] == email:
            otp = str(random.randint(100000, 999999))
            otp_storage[email] = otp

            print("OTP for", email, "is:", otp)  # TEMP

            return jsonify({"message": "OTP sent to email"}), 200

    return jsonify({"message": "Email not found"}), 404


# ================== VERIFY OTP ==================
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    if otp_storage.get(email) == otp:
        return jsonify({"message": "OTP verified"}), 200

    return jsonify({"message": "Invalid OTP"}), 400


# ================== RESET PASSWORD ==================
@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("new_password")

    for emp in employees:
        if emp["email"] == email:
            emp["password"] = new_password
            return jsonify({"message": "Password updated successfully"}), 200

    return jsonify({"message": "Error updating password"}), 400


# ================== DEPARTMENT ==================
@app.route("/departments", methods=["GET"])
def get_departments():
    return jsonify([d for d in departments if d["status"] == 1])


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


@app.route("/delete_department/<int:id>", methods=["DELETE"])
def delete_department(id):
    for d in departments:
        if d["dept_id"] == id:
            d["status"] = 0
            return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404


@app.route("/update_department/<int:id>", methods=["PUT"])
def update_department(id):
    data = request.json

    for d in departments:
        if d["dept_id"] == id:
            d["dept_name"] = data.get("dept_name")
            d["description"] = data.get("description")
            return jsonify({"message": "Updated"})

    return jsonify({"message": "Not found"}), 404


@app.route("/deleted_departments", methods=["GET"])
def deleted_departments():
    return jsonify([d for d in departments if d["status"] == 0])


@app.route("/restore_department/<int:id>", methods=["PUT"])
def restore_department(id):
    for d in departments:
        if d["dept_id"] == id:
            d["status"] = 1
            return jsonify({"message": "Restored"})
    return jsonify({"message": "Not found"}), 404


# ================== ROLE ==================
roles = [
    {
        "id": 1,
        "name": "Admin",
        "description": "Full access",
        "permissions": ["add", "edit", "delete"],
        "department_id": None,
        "status": "active"
    },
    {
        "id": 2,
        "name": "Employee",
        "description": "View only",
        "permissions": ["view"],
        "department_id": None,
        "status": "active"
    }
]

role_id_counter = 3


@app.route("/add_role", methods=["POST"])
def add_role():
    global role_id_counter
    data = request.json

    if not data.get("name"):
        return jsonify({"error": "Role name required"}), 400

    new_role = {
        "id": role_id_counter,
        "name": data.get("name"),
        "description": data.get("description"),
        "permissions": data.get("permissions", []),
        "department_id": data.get("department_id"),
        "status": "active"
    }

    roles.append(new_role)
    role_id_counter += 1

    return jsonify({"message": "Role added", "role": new_role})


@app.route("/get_roles", methods=["GET"])
def get_roles():
    return jsonify([r for r in roles if r["status"] == "active"])


@app.route("/get_deleted_roles", methods=["GET"])
def get_deleted_roles():
    return jsonify([r for r in roles if r["status"] == "deleted"])


@app.route("/update_role/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.json

    for role in roles:
        if role["id"] == role_id:
            role["name"] = data.get("name", role["name"])
            role["description"] = data.get("description", role["description"])
            role["permissions"] = data.get("permissions", role["permissions"])
            role["department_id"] = data.get("department_id", role["department_id"])

            return jsonify({"message": "Updated", "role": role})

    return jsonify({"error": "Role not found"}), 404


@app.route("/delete_role/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    for role in roles:
        if role["id"] == role_id:
            role["status"] = "deleted"
            return jsonify({"message": "Deleted"})
    return jsonify({"error": "Role not found"}), 404


@app.route("/restore_role/<int:role_id>", methods=["PUT"])
def restore_role(role_id):
    for role in roles:
        if role["id"] == role_id:
            role["status"] = "active"
            return jsonify({"message": "Restored"})
    return jsonify({"error": "Role not found"}), 404


# ================== EMPLOYEE ==================
employees = [
    {
        "id": 1,
        "first_name": "Admin",
        "last_name": "User",
        "username": "admin",
        "password": "1234",
        "email": "admin@gmail.com",
        "mobile": "9999999999",
        "dept_id": 1,
        "role_id": 1,
        "reporting_manager_id": None,
        "date_of_joining": "2024-01-01",
        "status": "active"
    },
    {
        "id": 2,
        "first_name": "Ali",
        "last_name": "Khan",
        "username": "ali",
        "password": "1234",
        "email": "ali@gmail.com",
        "mobile": "8888888888",
        "dept_id": 2,
        "role_id": 2,
        "reporting_manager_id": 1,
        "date_of_joining": "2024-02-01",
        "status": "active"
    }
]

employee_id_counter = 3


@app.route("/add_employee", methods=["POST"])
def add_employee():
    global employee_id_counter
    data = request.json

    new_employee = {
        "id": employee_id_counter,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "username": data.get("username"),
        "password": data.get("password"),
        "email": data.get("email"),
        "mobile": data.get("mobile"),
        "dept_id": data.get("dept_id"),
        "role_id": data.get("role_id"),
        "reporting_manager_id": data.get("reporting_manager_id"),
        "date_of_joining": data.get("date_of_joining"),
        "status": "active"
    }

    employees.append(new_employee)
    employee_id_counter += 1

    return jsonify({"message": "Employee added", "employee": new_employee})


@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify([e for e in employees if e["status"] == "active"])


@app.route("/deleted_employees", methods=["GET"])
def deleted_employees():
    return jsonify([e for e in employees if e["status"] == "inactive"])


@app.route("/update_employee/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json

    for emp in employees:
        if emp["id"] == id:
            emp.update(data)
            return jsonify({"message": "Employee updated", "employee": emp})

    return jsonify({"error": "Employee not found"}), 404


@app.route("/delete_employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    for emp in employees:
        if emp["id"] == id:
            emp["status"] = "inactive"
            return jsonify({"message": "Employee deleted"})
    return jsonify({"error": "Employee not found"}), 404


@app.route("/restore_employee/<int:id>", methods=["PUT"])
def restore_employee(id):
    for emp in employees:
        if emp["id"] == id:
            emp["status"] = "active"
            return jsonify({"message": "Employee restored"})
    return jsonify({"error": "Employee not found"}), 404


# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)