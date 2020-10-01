---
title: Sesijas
created: '2020-10-01T04:54:34.490Z'
modified: '2020-10-01T05:06:49.145Z'
---

# Sesijas
Lai lietotājs varētu palikt ielogojies mājaslapāt, kad vēlas atgriezties uz to, tam ir nepieciešams turēt lietotāja datus sesijā, sesija vienmēr glabāsies serverī un kad lietotājs atgriezīsies uz mājaslapu, tā automātiski tiks atjaunota.

## Kā izveidot sesiju
Pirmais, kas jaizdari ir jāimportē `session` bibliotēka no flask, piemērs.
```Python
from flask import Flask, redirect, url_for, render_template, request, session
```
Tālāk, lai sessiju varētu droši uzturēt ir jaizveido slepenā atslēga un to izdara ar `app.secret_key` definējot tās vērtību, ieteicami ar sarežģītu virkni (zem `app = Flask(__name__ )`):
```Python
app = Flask(__name__ )
app.secret_key = "hello"
```
Nākamais solis ir modificēt login lapu.
```Python
@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        usern = request.form["nm"] # Iegūt lietotāja vārdu
        session["user"] = usern # Izveidot sesiju
        return redirect(url_for("user")) # Pārvirzīt uz lietotāja lapu
    else:
        if "user" in session: # Ja lietotājs ir sesijā
            return redirect(url_for("user")) # Pārvirzīt
        # Ja nav sesija, tad pārvirzīt uz login lapu
        return render_template("login_form.html")
```
Pēdējais solis ir izveidot veidu kā izdzēst lietotāja sesiju
```Python
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))
```

