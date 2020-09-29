---
tags: [Main]
title: flask-sagatve
created: '2020-09-29T03:34:25.446Z'
modified: '2020-09-29T06:01:38.719Z'
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


---
# Izmantotie resursi
https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX [Video pamācība Flask lietošanai]
https://www.python.org/ [Python mājaslapa + Dokumentācija]
https://flask.palletsprojects.com/en/1.1.x/ [Flask mājaslapa + Dokumentācija]

# Termini
Backend - aizmugursistēma
