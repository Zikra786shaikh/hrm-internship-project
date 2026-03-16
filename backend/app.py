from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "HRM System Backend Running"

if __name__ == "__main__":
    app.run(debug=True)