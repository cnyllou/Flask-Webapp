---
title: Sesijas
created: '2020-10-01T04:54:34.490Z'
modified: '2020-10-01T07:39:42.692Z'
---

# Sesijas
Lai lietotājs varētu palikt ielogojies mājaslapāt, kad vēlas atgriezties uz to, tam ir nepieciešams turēt lietotāja datus sesijā, sesija vienmēr glabāsies serverī un kad lietotājs atgriezīsies uz mājaslapu, tā automātiski tiks atjaunota.

### Atceries!
Sesijas nav vieta, kur uzglabāt datus uz visu laiku.

## Kā izveidot sesiju
Pirmais, kas jaizdari ir jāimportē `session` bibliotēka no flask, piemērs.
```Python
from flask import Flask, redirect, url_for, render_template, request, session
```
Tālāk, lai sessiju varētu droši uzturēt ir jaizveido slepenā atslēga un to izdara ar `app.secret_key` definējot tās vērtību, ieteicami ar sarežģītu virkni (zem `app = Flask(__name__ )`):
```Python
app = Flask(__name__ )
app.secret_key = "heasda121daksdmasdapslda2llo"
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

Bieži vien šis standarda sesija garums ir par īsu, lai to pagarinātu pie bibliotekām jāpievieno
```Python
from datetime import timedelta
```

Tālāk jānosaka sesijas ilgumas ar
```Python
app = Flask(__name__ )
app.secret_key = "hello"
# 5 dienas sesija būs aktīva
app.permanent_session_lifetime = timedelta(days=5)
```

Lai šo paramentru aktivizētu ir arī jāpievieno `session.permanent = True`
```Python
@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        session.permanent = True # Šis nosaka vai noteiktais sesijas ilgums būs pieņemts
        usern = request.form["nm"]
        session["user"] = usern
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
            
        return render_template("login_form.html")
```


