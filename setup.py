from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/home")
@app.route("/")
def home():
    return render_template("main/index.html")

if __name__ == "__main__":
    app.run(debug=True)