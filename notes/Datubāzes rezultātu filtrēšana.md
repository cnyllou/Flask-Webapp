---
tags: [JavaScript]
title: Datubāzes rezultātu filtrēšana
created: '2020-10-11T10:51:16.501Z'
modified: '2020-10-11T11:54:11.480Z'
---

# Datubāzes rezultātu filtrēšana
Man ir vajadzīga filtrēšanas funkcija, kas filtrē inventāru pēc nosaukuma kāmēr lietotājs raksta nosaukumu meklēšanas lodziņā.
Diemžēl šeit es nevaru lietot Python, jo atšķirībā no JavaScript Python neizpildas pārlūkā.
- Pārlūki nesaprot Python
- Python tikai var renderēt mājaslapas šablonu un tālāk darbs priekš lietotāja mijiedarbības jāiedod JavaScript
## Kā es šo panākšu tagad?
Lietojot JavaScript tiks noklausīts lietotāja notikums, rakstīšana
- Uz notikuma `onkeyup=""`
- Noslēpt visus rezultātus, kur ievade neatbilst nosaukumam
```javascript
function listen_input() {
  // Deklarēt mainīgos
 var input, filter, container, item, name, i, txtValue;
 input = document.getElementById('user_input');
 filter = input.value.toUpperCase();
 container = document.getElementById("container");
 item = container.getElementsByClassName('catalog-item');

 // Iet cauri visiem vienumiem
for (i = 0; i < item.length; i++) {
  name = item[i].getElementsByClassName("item-name")[0];
  txtValue = name.textContent || name.innerText;
  if (txtValue.toUpperCase().indexOf(filter) > -1) {
    item[i].style.display = "";
  } else {
    item[i].style.display = "none";
  }
 }
}
```

