from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__ )
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        usern = request.form["nm"]
        session["user"] = usern
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
            
        return render_template("login_form.html")


@app.route("/user")
def user():
    if "user" in session:
        user_session = session["user"]
        return render_template("user_profile.html", username=user_session)
    else:
        return render_template("login_form.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(debug=True)