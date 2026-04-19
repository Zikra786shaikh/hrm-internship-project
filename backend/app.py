from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
import os
from datetime import datetime # Added for task timestamps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================== HOME ==================
@app.route("/")
def home():
    return "Backend Running"

# Existing OTP and Email functions remain exactly as you provided...
otp_storage = {}

def send_email_otp(receiver_email, otp):
    try:
        email_user = os.environ.get("EMAIL_ADDRESS")
        email_pass = os.environ.get("EMAIL_PASSWORD")
        if not email_user or not email_pass:
            return
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        message = f"Subject: HRM OTP\n\nYour OTP is: {otp}"
        server.sendmail(email_user, receiver_email, message)
        server.quit()
    except Exception as e:
        print("Email error:", e)

# Existing Departments, Roles, and Employees remain exactly as you provided...
# (Keep your existing departments, roles, and employees lists here)

# ================== TASK MANAGEMENT STORAGE ==================
# Data structures based on [cite: 3, 5]
tasks = []
task_assignments = []
task_id_counter = 1
assignment_id_counter = 1

# ================== TASK MODULE ROUTES ==================

@app.route("/add_task", methods=["POST"])
def add_task():
    global task_id_counter, assignment_id_counter
    data = request.json
    
    # 1. Create the Task 
    new_task = {
        "task_id": task_id_counter,
        "task_title": data.get("task_title"),
        "task_description": data.get("task_description"),
        "task_priority": data.get("task_priority"), # High, Medium, Low [cite: 19]
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "task_type": data.get("task_type"), # Individual or Team [cite: 22]
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": 1 # For soft delete
    }
    tasks.append(new_task)

    # 2. Create the Task Assignment [cite: 5]
    # 'employee_id' comes from the "Assigned To" dropdown [cite: 12, 20]
    new_assignment = {
        "assignment_id": assignment_id_counter,
        "task_id": task_id_counter,
        "employee_id": data.get("employee_id"), 
        "assigned_by": data.get("assigned_by"), # The logged-in user's ID
        "assigned_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending", # Default status [cite: 53]
        "completed_at": None
    }
    task_assignments.append(new_assignment)
    
    task_id_counter += 1
    assignment_id_counter += 1
    return jsonify({"message": "Task created and assigned successfully"}), 201

@app.route("/get_dashboard_tasks", methods=["GET"])
def get_dashboard_tasks():
    # Requirements: Pagination, Multiple Filters, Statistics [cite: 67, 74, 75]
    user_id = int(request.args.get("user_id"))
    role = request.args.get("role")
    
    # Filter by Employee/Status/Date [cite: 68, 70, 72]
    filter_employee = request.args.get("employee_id")
    filter_status = request.args.get("status")
    filter_from_date = request.args.get("from_date")
    filter_to_date = request.args.get("to_date")

    # RBAC logic [cite: 107]
    # Admin sees all. Managers see reporting employees. Employees see only their own.
    filtered_assignments = task_assignments
    if role == "Employee":
        filtered_assignments = [a for a in task_assignments if a["employee_id"] == user_id]
    elif role == "Manager":
        # Only show employees reporting to this manager 
        reporting_ids = [e["id"] for e in employees if e["reporting_manager_id"] == user_id]
        filtered_assignments = [a for a in task_assignments if a["employee_id"] in reporting_ids]

    # Apply additional filters [cite: 75]
    if filter_employee:
        filtered_assignments = [a for a in filtered_assignments if a["employee_id"] == int(filter_employee)]
    if filter_status:
        filtered_assignments = [a for a in filtered_assignments if a["status"] == filter_status]

    # Build final list joining tasks and assignments
    result = []
    for a in filtered_assignments:
        task = next((t for t in tasks if t["task_id"] == a["task_id"] and t["status"] == 1), None)
        if task:
            # Get employee name for the dashboard table [cite: 29]
            emp = next((e for e in employees if e["id"] == a["employee_id"]), None)
            emp_name = f"{emp['first_name']} {emp['last_name']}" if emp else "Unknown"
            
            result.append({
                "task_id": task["task_id"],
                "employee_name": emp_name,
                "task_title": task["task_title"],
                "start_date": task["start_date"],
                "end_date": task["end_date"],
                "status": a["status"],
                "priority": task["task_priority"]
            })

    # Stats logic [cite: 74]
    stats = {
        "total": len(result),
        "completed": len([r for r in result if r["status"] == "Completed"]),
        "pending": len([r for r in result if r["status"] == "Pending"]),
        "in_progress": len([r for r in result if r["status"] == "In Progress"])
    }

    # Pagination: 10 records per page [cite: 67]
    page = int(request.args.get("page", 1))
    start = (page - 1) * 10
    end = start + 10

    return jsonify({
        "tasks": result[start:end],
        "statistics": stats,
        "total_pages": (len(result) // 10) + (1 if len(result) % 10 > 0 else 0)
    })

@app.route("/update_task/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json # Contains updated fields [cite: 150]
    for t in tasks:
        if t["task_id"] == id:
            t["task_title"] = data.get("task_title", t["task_title"])
            t["task_description"] = data.get("task_description", t["task_description"])
            t["task_priority"] = data.get("task_priority", t["task_priority"])
            t["start_date"] = data.get("start_date", t["start_date"])
            t["end_date"] = data.get("end_date", t["end_date"])
            t["task_type"] = data.get("task_type", t["task_type"])
            t["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update assignment status if changed
            for a in task_assignments:
                if a["task_id"] == id:
                    a["status"] = data.get("status", a["status"])
                    if a["status"] == "Completed":
                        a["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"message": "Task updated successfully"}) [cite: 151]
    return jsonify({"message": "Task not found"}), 404

@app.route("/delete_task/<int:id>", methods=["DELETE"])
def delete_task(id):
    # Soft delete logic to match your other modules
    for t in tasks:
        if t["task_id"] == id:
            t["status"] = 0 
            return jsonify({"message": "Task deleted successfully"}) [cite: 153]
    return jsonify({"message": "Task not found"}), 404

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)