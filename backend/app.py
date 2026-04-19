from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================== STORAGE (In-Memory) ==================
otp_storage = {}

departments = [
    {"dept_id": 1, "dept_name": "HR", "description": "Human Resource", "status": 1},
    {"dept_id": 2, "dept_name": "IT", "description": "Tech", "status": 1}
]
next_id = 3

roles = [
    {"id": 1, "name": "Admin", "description": "Full access", "permissions": ["add", "edit", "delete"], "status": "active"},
    {"id": 2, "name": "Manager", "description": "Team management", "permissions": ["view", "add"], "status": "active"},
    {"id": 3, "name": "Employee", "description": "View only", "permissions": ["view"], "status": "active"}
]
role_id_counter = 4

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

tasks = [
    {"task_id": 1, "task_title": "Database Design", "task_description": "Create SQL schema", "task_priority": "High", "start_date": "2026-04-01", "end_date": "2026-04-10", "task_type": "Individual", "status": 1},
    {"task_id": 2, "task_title": "API Integration", "task_description": "Connect frontend", "task_priority": "Medium", "start_date": "2026-04-05", "end_date": "2026-04-12", "task_type": "Individual", "status": 1},
    {"task_id": 3, "task_title": "UI Bug Fixes", "task_description": "Fix alignment", "task_priority": "Low", "start_date": "2026-04-15", "end_date": "2026-04-20", "task_type": "Team", "status": 1},
    {"task_id": 4, "task_title": "Security Audit", "task_description": "Check vulnerabilities", "task_priority": "High", "start_date": "2026-04-18", "end_date": "2026-04-25", "task_type": "Individual", "status": 1}
]

task_assignments = [
    {"assignment_id": 1, "task_id": 1, "employee_id": 2, "assigned_by": 1, "status": "Completed"},
    {"assignment_id": 2, "task_id": 2, "employee_id": 3, "assigned_by": 1, "status": "Pending"},
    {"assignment_id": 3, "task_id": 3, "employee_id": 2, "assigned_by": 1, "status": "In Progress"},
    {"assignment_id": 4, "task_id": 4, "employee_id": 3, "assigned_by": 1, "status": "Pending"}
]

task_id_counter = 5
assignment_id_counter = 5

# ================== HELPER FUNCTIONS ==================
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

# ================== ROUTES ==================
@app.route("/")
def home():
    return "Backend Running"

@app.route("/test_env")
def test_env():
    return {
        "email": os.environ.get("EMAIL_ADDRESS"),
        "status": "working"
    }

# --- Department Management ---
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

# --- Role Management ---
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

# --- Employee Management ---
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

# --- Authentication ---
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for emp in employees:
        if emp["username"] == username and emp["status"] == "active":
            if check_password_hash(emp["password"], password):
                # Mapping roles based on role_id
                role_label = "Admin" if emp["role_id"] == 1 else "Manager" if emp["role_id"] == 2 else "Employee"
                return jsonify({"message": "Login successful", "role": role_label, "id": emp["id"]})

    return jsonify({"message": "Invalid credentials"}), 401

# --- Password Reset ---
@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")
    for emp in employees:
        if emp["email"] == email:
            otp = str(random.randint(100000, 999999))
            otp_storage[email] = otp
            send_email_otp(email, otp)
            return jsonify({"message": "OTP sent"}), 200
    return jsonify({"message": "Email not found"}), 404

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    if otp_storage.get(data.get("email")) == data.get("otp"):
        return jsonify({"message": "OTP verified"}), 200
    return jsonify({"message": "Invalid OTP"}), 400

@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    for emp in employees:
        if emp["email"] == data.get("email"):
            emp["password"] = generate_password_hash(data.get("new_password"))
            return jsonify({"message": "Password updated"}), 200
    return jsonify({"message": "Error"}), 400

# --- Task Management ---
@app.route("/add_task", methods=["POST"])
def add_task():
    global task_id_counter, assignment_id_counter
    data = request.json
    new_task = {
        "task_id": task_id_counter,
        "task_title": data.get("task_title"),
        "task_description": data.get("task_description"),
        "task_priority": data.get("task_priority"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "task_type": data.get("task_type"),
        "status": 1
    }
    tasks.append(new_task)
    new_assignment = {
        "assignment_id": assignment_id_counter,
        "task_id": task_id_counter,
        "employee_id": int(data.get("employee_id")),
        "assigned_by": int(data.get("assigned_by")),
        "status": "Pending"
    }
    task_assignments.append(new_assignment)
    task_id_counter += 1
    assignment_id_counter += 1
    return jsonify({"message": "Task created"}), 201

@app.route("/get_dashboard_tasks", methods=["GET"])
def get_dashboard_tasks():
    u_id = int(request.args.get("user_id", 0))
    role = request.args.get("role", "Employee")
    f_status = request.args.get("status")
    f_emp = request.args.get("employee_id")

    filtered = task_assignments
    if role == "Manager":
        reports = [e["id"] for e in employees if e.get("reporting_manager_id") == u_id]
        filtered = [a for a in task_assignments if a["employee_id"] in reports]
    elif role == "Employee":
        filtered = [a for a in task_assignments if a["employee_id"] == u_id]

    if f_status: 
        filtered = [a for a in filtered if a["status"] == f_status]
    if f_emp: 
        filtered = [a for a in filtered if a["employee_id"] == int(f_emp)]

    result = []
    for a in filtered:
        t = next((task for task in tasks if task["task_id"] == a["task_id"] and task["status"] == 1), None)
        if t:
            emp = next((e for e in employees if e["id"] == a["employee_id"]), None)
            result.append({
                **t, 
                "status": a["status"], 
                "employee_name": f"{emp['first_name']} {emp['last_name']}" if emp else "Unknown"
            })

    stats = {
        "total": len(result),
        "pending": len([r for r in result if r["status"] == "Pending"]),
        "in_progress": len([r for r in result if r["status"] == "In Progress"]),
        "completed": len([r for r in result if r["status"] == "Completed"])
    }
    return jsonify({"tasks": result, "statistics": stats})

@app.route("/delete_task/<int:id>", methods=["DELETE"])
def delete_task(id):
    for t in tasks:
        if t["task_id"] == id:
            t["status"] = 0
            return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)