from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from admin.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3' # users - table name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view", methods=["POST", "GET"])
def view():
    if request.method == "POST":
        delete_user = request.form["delete_user"]
        add_username = request.form["add_username"]
        add_email = request.form["add_email"]

        found_username = users.query.filter_by(name=add_username).first() 
        found_email = users.query.filter_by(name=add_email).first() 
        if found_username or found_email:
            flash("Username [ {add_username} ] or [ {add_email} ] already in database")
        else:
            usr = users(add_username, add_email)
            db.session.add(usr)
            db.session.commit()

        try:
            if delete_user != "":
                found_user_delete = users.query.filter_by(name=delete_user).first()
                db.session.delete(found_user_delete)
                db.session.commit() 
                flash(f"User [ {delete_user} ] was deleted!")
                #return redirect(url_for('view'))
        except:
            flash(f"User [ {delete_user} ] not in database!")
        

    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first() # Atrod lietotājus ar ierakstīto vārdu
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit() # Pie visām datu bāzes izmaiņām jāraksta apstiprinājums

        flash("Login successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
            
        return render_template("login_form.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit() 
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user_profile.html", email=email)
    else:
        flash("You are not logged in!")
        return render_template("login_form.html")


@app.route("/logout")
def logout():
    if "user" in session:
        flash("You have been logged out!", "info")
        session.pop("user", None)
        session.pop("email" , None)
    else:
        flash("You are already logged out!", "info")

    return redirect(url_for("login_page"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)