from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================== HOME ==================
@app.route("/")
def home():
    return "Backend Running"

# ================== TEST ENV ==================
@app.route("/test_env")
def test_env():
    return {
        "email": os.environ.get("EMAIL_ADDRESS"),
        "status": "working"
    }

# ================== OTP STORAGE ==================
otp_storage = {}

# ================== EMAIL FUNCTION ==================
def send_email_otp(receiver_email, otp):
    try:
        email_user = os.environ.get("EMAIL_ADDRESS")
        email_pass = os.environ.get("EMAIL_PASSWORD")

        if not email_user or not email_pass:
            print("ENV NOT SET - skipping email")
            return

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)

        message = f"Subject: HRM OTP\n\nYour OTP is: {otp}"
        server.sendmail(email_user, receiver_email, message)
        server.quit()

    except Exception as e:
        print("Email error:", e)

# ================== DEPARTMENT ==================
departments = [
    {"dept_id": 1, "dept_name": "HR", "description": "Human Resource", "status": 1},
    {"dept_id": 2, "dept_name": "IT", "description": "Tech", "status": 1}
]
next_id = 3

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

# ================== ROLES ==================
roles = [
    {"id": 1, "name": "Admin", "description": "Full access", "permissions": ["add", "edit", "delete"], "status": "active"},
    {"id": 2, "name": "Employee", "description": "View only", "permissions": ["view"], "status": "active"}
]
role_id_counter = 3

@app.route("/get_roles", methods=["GET"])
def get_roles():
    return jsonify([r for r in roles if r["status"] == "active"])

@app.route("/add_role", methods=["POST"])
def add_role():
    global role_id_counter
    data = request.json

    new_role = {
        "id": role_id_counter,
        "name": data.get("name"),
        "description": data.get("description"),
        "permissions": data.get("permissions", []),
        "status": "active"
    }

    roles.append(new_role)
    role_id_counter += 1
    return jsonify({"message": "Role added"})

@app.route("/delete_role/<int:id>", methods=["DELETE"])
def delete_role(id):
    for r in roles:
        if r["id"] == id:
            r["status"] = "deleted"
            return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404

@app.route("/restore_role/<int:id>", methods=["PUT"])
def restore_role(id):
    for r in roles:
        if r["id"] == id:
            r["status"] = "active"
            return jsonify({"message": "Restored"})
    return jsonify({"message": "Not found"}), 404

# ================== EMPLOYEES ==================
employees = [
    {
        "id": 1,
        "first_name": "Admin",
        "last_name": "User",
        "username": "admin",
        "password": generate_password_hash("1234"),
        "email": "admin@gmail.com",
        "mobile": "9999999999",
        "dept_id": 1,
        "role_id": 1,
        "reporting_manager_id": None,
        "date_of_joining": "2024-01-01",
        "status": "active"
    }
]
employee_id_counter = 2

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify([e for e in employees if e["status"] == "active"])

@app.route("/add_employee", methods=["POST"])
def add_employee():
    global employee_id_counter
    data = request.json

    new_emp = {
        "id": employee_id_counter,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "username": data.get("username"),
        "password": generate_password_hash(data.get("password")),
        "email": data.get("email"),
        "mobile": data.get("mobile"),
        "dept_id": data.get("dept_id"),
        "role_id": data.get("role_id"),
        "reporting_manager_id": data.get("reporting_manager_id"),
        "date_of_joining": data.get("date_of_joining"),
        "status": "active"
    }

    employees.append(new_emp)
    employee_id_counter += 1
    return jsonify({"message": "Employee added"})

# ================== LOGIN ==================
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for emp in employees:
        if emp["username"] == username and emp["status"] == "active":
            if check_password_hash(emp["password"], password):

                role = "Admin" if emp["role_id"] == 1 else "Manager" if emp["role_id"] == 2 else "Employee"

                return jsonify({"message": "Login successful", "role": role})

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

            try:
                send_email_otp(email, otp)
            except:
                print("Email failed")

            return jsonify({"message": "OTP sent"}), 200

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
            emp["password"] = generate_password_hash(new_password)
            return jsonify({"message": "Password updated"}), 200

    return jsonify({"message": "Error"}), 400

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)