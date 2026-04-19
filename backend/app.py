from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import smtplib
import os

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route("/")
def home():
    return "Backend Running"
@app.route("/test_env")
def test_env():
    return {
        "email": os.environ.get("EMAIL_ADDRESS"),
        "status": "working"
    }


# ================== OTP STORAGE ==================
otp_storage = {}

# ================== EMAIL CONFIG ==================
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

        message = f"Subject: HRM OTP\n\nOTP: {otp}"

        server.sendmail(email_user, receiver_email, message)
        server.quit()

    except Exception as e:
        print("Email error:", e)
# ================== EMPLOYEES (UPDATED WITH HASHING) ==================
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


# ================== LOGIN (SECURE) ==================
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for emp in employees:
        if emp["username"] == username and emp["status"] == "active":

            if check_password_hash(emp["password"], password):

                role = "Admin" if emp["role_id"] == 1 else "Manager" if emp["role_id"] == 2 else "Employee"

                return jsonify({
                    "message": "Login successful",
                    "role": role
                })

    return jsonify({"message": "Invalid credentials"}), 401


# ================== FORGOT PASSWORD (REAL GMAIL OTP) ==================
@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    # check if email exists
    for emp in employees:
        if emp["email"] == email:

            otp = str(random.randint(100000, 999999))
            otp_storage[email] = otp

            try:
                send_email_otp(email, otp)
            except:
                print("OTP email failed but app continues")

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


# ================== RESET PASSWORD (HASHED) ==================
@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("new_password")

    for emp in employees:
        if emp["email"] == email:

            emp["password"] = generate_password_hash(new_password)

            return jsonify({"message": "Password updated successfully"}), 200

    return jsonify({"message": "Error updating password"}), 400


# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)