---
tags: [Datubāze]
title: Datu ģenerēšana
created: '2020-10-05T04:07:43.744Z'
modified: '2020-10-10T12:20:35.880Z'
---

# Datu ģenerēšana
# Kā es ģenerēju datus priekš datubāzes
1. Vispirms viss tiek sarakstīts MS Excel
2. Eksportēšana uz CSV datni
3. Ar python ciklu
- CSV datnes saturs tiek nolasīts 
- Lauku saturs tiek ievietots mainīgajos
- Ar `INSERT INTO users` tiek ievietots sqlite3 datubāzē

# Datu ģenerēšana iekš excel un ar Python skriptiem
# Darbinieku tabula un tam saistītās tabulas
**Lietotājvārdi:**
```=D2&"."&E2```

**Secības maiņa:**
1. Blakus kolonnā ierakstīt formulu `=RAND()`
2. Iezīmēt visu rindu ar skaitļiem
3. Sakārtot skaitļus dilstošā vai augošā secībā
4. Blakus kolonnai jābūt arī ietekmētai

**Paroles:**
1. Iekopēt izmantotākās paroles
2. Ar Python skriptu 'hashot' paroles un ievietot citā failā
3. Ievietot paroļu hashus datubāzē

**Personas Kodi:**
- Python skripts
1. Ar Excel Data Analysis tiek ģenerēti vecumi no 20 līdz 40 diapazonam
2. Skripts nolasa šos vecumus
3. Dienas un mēness cipari tiek uzģenerēti nejaušā secībā un savienoti ar gadu cipariem
4. Tiek pievienota otrā daļa

**E-pasti:**
Tiek savienots lietotajvards ar darba e-pasta domenu

**Profila bildes:**
Iekopēts noklusējuma bildes ceļš datorā, ko lietotājs pēc tam varēs pats pārmainīt

### Darbinieki:
- Datubāzē glabājas 199 darbinieki

## Pilsētas/biroji
Pilsētu tabulu izmantoju, lai aprēķinātu cik darbinieki varētu atrasties kātrā pilsētas birojā un pēc tam skatoties uz skaitu, ierakstīju 3 rīgas birojus, jo darbinieku skaits bija vislielākais (129 darb. uz 3 birojiem)
### Process:
1. Pēc iedzīvotāju skaita statistikas atradu 8 pilsētas, kur ir visvairāk iedzīvotāju
2. ar `=SUM()` aprēķināju kopējo skaitu ar iedzīvotājiem visās pilsētās
3. `=E2/$J$2` - Izvilku procentuālu vērtību
4. `=F2*$J$1` - Katru procentuālo vērtību sareizināju ar kopējo darbinieku skaitu
- Šādi ieguvu darbinieku skaitu uz pilsētas birojiem
- Tagad man vajag 199 `biroj_id` laukiem tik daudz vērtēbas, cik uz katru biroju ir darbinieki
1. Lai atkārtu `biroj_id` vērtību * darb. sk. sekoju līdzi pamācībai
    - https://www.excelhow.net/repeat-cell-value-n-times-in-excel.html
    - `=VLOOKUP(H2;$E$2:$F$12;2)`
2. Nejaušā secība sakārtoju šo kolonnu ar blakus kolonnas vērtību no `=RAND()`
    - ! Šīs `biroj_id` saturu jāpārvērš par ciparu vērtībām vispirms
- Tagad, kad dati ir sajaukti, varu tos pārkopēt `t_lietotāji` tabulā

## Projekti tabula
Paši projekta nosaukumi tiek ņemti no saraksta ar uzņēmumiem
Projektu skaits tiek ņemts vērā balstoties uz to, no cik cilvēkiem sastāvētu ideāla komanda (5-6 cilvēku komanda)
Šājā 199 cilvēku uzņēmumā būs 39 projekti, kas tiek aprēķināts ar Python skriptu.
* Pēdējais 40 projekts (NAV PIESAISTĪTS) ir domāts priekš administratora

### Kā tiek piešķirti projekti darbiniekiem?
Projektu aprēķināšana un piešķiršana pie birojiem tiek veikta ar Python skriptu
**Kā tas darbojas?**
- Jāskatās, cik cilvēki ir katrā birojā
- Loģiski jāsadala projekts cilvēkiem, kas atrodas birojos, kur ir 5-6 cilvēki vai vairāk
    - Ja ir mazāk nekā vai 6 cilvēki vienā birojā, tad komanda sastāvēs no visa biroja
    - Ja ir vairāk tad tiks paņemti 5 vai 6 cilvēki un atlikums būs piesaistīts pie cita projekta
        - minimālais cilvēku skaits projektā ir 5
        - Ja birojā nav pietiekami, tad tiek paņemti cilvēki no nākošā


## Pozīcijas un to piešķiršana
- Administrators - Lietotājs ar visām tiesībām gan mājaslapā, gan datubāzē
- Projekta vadītājs - Darbinieka tiesības + Tiesības piesaistīt ierīces uz projektu
- Darbinieks - Tiesības piesaistīt inventāru uz savu vārdu
Saistīšana ar lietotāju tabulu ir vienkārša, katrā projektā 1 projekta vadītājs, 1 administrators un pārējie ir darbinieki


# Invetāra tabula `t_vienumi` un tam saistītās tabulas
**Svītrs kods**
- Python skripts, kas uzģenerē 12 skaitļu virkni pēc nejaušības
## Kā tas tiek izdarīts no mājaslapas puses, kad lietotājs ievada to
- Lietotājs šo lauku neaiztiek
- Ar Python

**Preču nosaukumi**
- Ejot cauri interneta veikaliem un sarakstiem ar ražotāju precēm, manuāli savadīts
- Priekš modelis laukiem arī tika izmantota Excel komanda `="CNN"&RANDBETWEEN(51;99)&"A/"&RANDBETWEEN(0;99)&"P"`, kuriem lauks bija tukšs, iespējams modeļa nosaukums

**Ražotāju saraksts**
- Tika meklēti saraksti ar mobilo telefonu ražotājiem un tam līdzīgi uz citiem invetāra tipiem

**Kategorijas**
- Loģiski apvienotas inventāra kategorijas, lai darbinieks varētu atrast, ko vajag bez problēmām


**Birojs, kur atrodas**
- Loģiski sakārtots pēc tā, cik cilvēki atrodas uz biroju

## Ieraksti tabula
Šī tabula uzglabā ierakstus ar lietotāju rīcībām, piemēram, kad lietotājs rediģē, pievieno, paņem, atgriež inventāru, tiek veikts jauns ieraksts, kur tiek ņemts vērā vienums, lietotājs, darbība un norises laiks (automātiski pievienojas no ieraksta izveidošanas)
Kā noklusējumā importējot datus tiks piereģistrēts, ka root lietotājs pievienoja katru vienumu vienā laikā.




# Izmantotie resursi
- https://www.excelhow.net/repeat-cell-value-n-times-in-excel.html
- https://cuttingedgepr.com/whats-ideal-number-people-work-team-committee/
- https://www.csb.gov.lv/lv/statistika/statistikas-temas/iedzivotaji/iedzivotaju-skaits/galvenie-raditaji/iedzivotaju-skaits-republikas-pilsetas


