---
tags: [Main]
title: flask-sagatve
created: '2020-09-29T03:34:25.446Z'
modified: '2020-10-01T05:09:03.350Z'
---

# Flask sagatavošana
---
# Pieraksti
- Python būs aizmugursistēmas serveris, kas uzturēs mājaslapu


# Pirms sāc
- Jābūt Python ieinstalētam datorā
- Jābūt interneta pārlūkam

# Instrukcija iesākšanai
1. `pip install flask`
2. Izveidot mape un tajā izveidot Python datni `main.py`("main" vietā jebkas var būt)
3. Atvērt `main.py` un ierakstīt sekojošu, lai varētu startēt Python serveri
```Python
from flask import Flask

app = Flask(__name__ )

@app.route("/")
def home():
    return "Šī ir mana mājaslapa"

if __name__ == "__main__":
    app.run()
```
4. Tālāk caur termināli:
- Aiziet uz mapi, kur atrodas Python datne
- Rakstīt `python main.py`
- Tiks ieslēgts Python serveris un tālāk būs Pārlūkā jāiekopē piedāvātā mājaslapas adrese
` http://127.0.0.1:5000/`

# Iespējas ar Flask
- Rakstīt Python kodu iekšā `.html` datnē
```html
<!DOCTYPE html>
<html>
<head>
    <title>Home page</title>
</head>
<body>
    <h1>Hello {{content}}</h1>
    <h2>This is my basic HTML home page</h2>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Recusandae aliquid ab ipsa nam cum laboriosam temporibus doloribus minus, inventore corrupti reiciendis expedita molestiae, beatae, ratione optio quasi explicabo sit sunt?</p>
    {% for x in range(0, 10) %}
        <p>Hello  </p>
    {% endfor %}
</body>
</html>
```
- Automātiski atjaunot mājaslapu kamēr tiek rakstīts kods, šajā veidā nav vajadzība restartēt serveri ik pēc katras izmaiņas
```Python
if __name__ == "__main__":
    app.run(debug=True) # Iedodot `debug=True` parametru
```



---
# Izmantotie resursi
https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX [Video pamācība Flask lietošanai]
https://www.python.org/ [Python mājaslapa + Dokumentācija]
https://flask.palletsprojects.com/en/1.1.x/ [Flask mājaslapa + Dokumentācija]

# Termini
Backend - aizmugursistēma
