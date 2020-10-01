---
title: ./static mape
created: '2020-10-01T12:19:04.078Z'
modified: '2020-10-01T12:26:02.329Z'
---

# `./static` mape
`./static` mape ir mape, kur flask meklēs 'css' un 'js' datnes, ja datnes būs citā mapē, tad tās netiks izmantotas.

Arī ir svarīgi, kā defināt šo datņu atrašanās vietu, tas ir nedaudz citādāk, nekā standarda html.

Lietojot flask html lapu šablonu, css definēšana izskatīsies šādi:
```HTML
<!DOCTYPE html>
<html>
<head>
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
  <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```
href atribūtam dodot vērtību 
`href="{{ url_for('static', filename='style.css') }}"`

## Izmaiņas nenotiek!?
Tam ir vienkārš risinājums vai nu iztīrot pārlūka kešatmiņu, vai vēl vienkāršāk ar `CTRL + SHIFT + R`
