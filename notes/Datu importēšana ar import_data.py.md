---
tags: [Datubāze]
title: Datu importēšana ar import_data.py
created: '2020-10-07T07:53:38.752Z'
modified: '2020-10-20T08:25:44.889Z'
---

# Datu importēšana ar `import_data.py`
---
Priekš datu importēšanas es uzrakstīju Python skriptu `import_data.py` un to apvienoju ar flask, lai to varētu izmantot kā flask commandu `flask import-data`.

## Vispirs darāmais!
- Sagatavot .csv/.txt datni un ielikt to `Flask/trakeris/import_data` mapē

## Ievads importēšanas procesam
Ierakstot `flask import-data` komandlīnijā es aktivizēju savu 'Import Wizard'
```cmd
(venv) C:\Users\TERMINAL\Desktop\notes\Flask>flask import-data
IMPORT WIZARD ACTIVATED.
Sintakse priekš importa ir sekojoša:
datne tabula kol1,kol2,..,kol9
```
Tālāk man ir jāievada:
datne - .csv/.txt datnes nosaukums
tabula - tabulas nosaukums, kas eksistē datubāzē
col1,.. - kolonnas nosaukums
  - Obligāti pēc katra nosaukuma komatu, bez atstarpēm! (ja ir vairāk par 1)

Pēc datu noteikšanas tiek izvadīti, dati kā izskatās masīvā, tas ir, lai pārbaudītu kā šie dati tiks padoti tālāk, ja ir nevajadzīgi artifakti, tad pēc prasītā: 
```
Atgriezt kā ir vai formatēt? (y, f)
```
Ir jāievada 'f', kur pēc tam tiek formatēti dati priekš apstrādāšanas un lietotājam tiek parādīts SQL vaicājums, ko pēc tam lietotājs apstiprina vai rediģē:
- Rediģējot lietotājs var:
  - Ierakstīt savu vaicājumu un apstiprināt 
    - y - Turpināt ar savu
    - n - Atcelt programmas darbību
    - a - Turpināt ar iepriekšējo
```cmd
Tavs vaicājums:
 INSERT INTO tabula (col1,col2) VALUES (?, ?)
Turpināt vai rediģēt? (r - rediģēt)
```

```cmd
Apstriprināt? (y, a - izmantot iepriekšējo, n - atcelt darbību)
y
Tiek izmantots vaicājums:
INSERT INTO atasd (col2, col2) VALUES (?, ?)
```
Nobeigumā, pēc šīs operācijas, dati tiek ievadīti datubāzē un tiek izvadīta šī tabula ar SQL vaicājumu.
```sql
SELECT * FROM tabula
```

# Importa secība (Nav tik ļoti svarīga)
- Vispirms tabulas bez `FOREIGN KEY` un šīm referencēm
- Pēc tam pārējās, lai nekas nenojuktu ar saitēm
- Eksportēt visas tabulas kā `.csv`
1. Bez `FOREIGN KEY` tabulas
- t_pilsetas
pils_id,pilseta
- t_projekti
proj_id,projekts
- t_pozicijas
poz_id,pozicija
- t_darbibas 
darb_id,darbiba
- t_kategorijas 
kateg_id,kategorija
- t_razotaji 
razot_id,razotajs
- t_statusi 
stat_id,status


2. Tagad droši varu importēt datus priekš tabulām ar relācijām
- t_lietotaji
liet_id,lietv,parole,vards,uzv,poz_id,proj_id,biroj_id,pers_kods,epasts,tel_num,profil_bild_cels
- t_biroji
biroj_id,birojs,pils_id
- t_vienumi
vienum_id,svitr_kods,vienum_nosauk,modelis,razot_id,iss_aprakst,detalas,komentars,kateg_id,biroj_id,liet_id,bilde_cels,nopirkt_dat
- t_ieraksti
ierakst_id,vienum_id,liet_id,darb_id

3. Kuras kolonnas?
- Praktiski visas izņemot tās, kurām ir noklusējuma vērtība kā `DEFAULT CURRENT_TIMESTANP`

