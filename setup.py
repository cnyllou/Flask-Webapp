from flask import Flask, render_template, url_for, request
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

def load_user(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        if valid_login(request.form['email'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = "Invalid username/password"
    
    return render_template("auth/login.html", error=error)

@app.route("/home")
@app.route("/")
def home():
    return render_template("main/index.html")

if __name__ == "__main__":
    app.run(debug=True)