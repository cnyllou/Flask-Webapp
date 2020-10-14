---
tags: [Datubāze, SQL]
title: SQL vaicājumi un saites
created: '2020-10-09T18:32:21.949Z'
modified: '2020-10-14T19:12:02.417Z'
---

# SQL vaicājumi un saites
Tabula **t_lietotaji**
```SQL
SELECT l.liet_id,
       lietv,
       parole,
       vards,
       uzv,
       poz.pozicija,
       pro.projekts,
       b.birojs,
       pers_kods,
       epasts,
       tel_num,
       profil_bild_cels
  FROM t_lietotaji l
       JOIN
       t_pozicijas poz ON l.poz_id = poz.poz_id
       JOIN
       t_projekti pro ON l.proj_id = pro.proj_id
       JOIN
       t_biroji b ON l.biroj_id = b.biroj_id;
```

Tabula **t_biroji**
```SQL
SELECT biroj_id,
       birojs,
       p.pilseta
  FROM t_biroji b
       JOIN
       t_pilsetas p ON b.pils_id = p.pils_id;
```

Tabula **t_vienumi**
```SQL
SELECT vienum_id,
       svitr_kods,
       vienum_nosauk,
       modelis,
       r.razotajs,
       iss_aprakst,
       detalas,
       komentars,
       k.kategorija,
       b.birojs,
       l.lietv,
       bilde_cels,
       nopirkt_dat
  FROM t_vienumi v
       JOIN
       t_razotaji r ON v.razot_id = r.razot_id
       JOIN
       t_kategorijas k ON v.kateg_id = k.kateg_id
       JOIN
       t_biroji b ON v.biroj_id = b.biroj_id
       JOIN
       t_lietotaji l ON v.liet_id = l.liet_id;
```

Tabula **t_ieraksti**
```SQL
SELECT i.ierakst_id,
       v.vienum_nosauk,
       l.lietv,
       d.darbiba
  FROM t_ieraksti i
       JOIN
       t_vienumi v ON i.vienum_id = v.vienum_id
       JOIN
       t_lietotaji l ON i.liet_id = l.liet_id
       JOIN
       t_darbibas d ON i.darb_id = d.darb_id;
```
--- 
# Tabulas ar relācijām
- **t_lietotaji** saites:
    - poz_id - pozīcija
    - proj_id - projekts
    - biroj_id - birojs
- **t_biroji** saites:
    - pils_id - pilsēta
- **t_vienumi** saites:
    - razot_id - ražotājs
    - kateg_id - kategorija
    - biroj_id - birojs
    - liet_id - lietotājvārds
- **t_ieraksti** saites:
    - vienum_id - vienuma nosaukums
    - liet_id - lietotājvārds
    - darb_id - darbība


---
# Citi SQL vaicājumi, kurus man gadijās lietot
Visu tabulas kolonnu pārvērš uz mazajiem burtiem
```SQL
UPDATE t_lietotaji
   SET lietv = LOWER(lietv),
       epasts = LOWER(epasts);
```
Lietotājam papildinot invetāru vajag unikālu svītrkodu
- Tiek atgriezts lielākais skaitlis no kolonnas svitr_kods, pieskaitas 1
```SQL
SELECT MAX(svitr_kods)+1 AS lielakais_cip
  FROM t_vienumi;
```
Iegūt kategoriju sarakstu no datubāzes
```SQL
SELECT kateg_id,
       kategorija
  FROM t_kategorijas;
```
Ievietot jaunus ierakstus, kur tiek dati ņemti no citām tabulām
- Tabulu ID meklēšana
```SQL
SELECT * FROM t_biroji WHERE birojs = ?;
SELECT * FROM t_kategorijas WHERE kategorija = ?;
```
- Tā kā lietotājs pats var ierakstīt ražotāju, atrastais tiks salīdzināts ar pārvēršot burtus uz mazajiem, lai neveidotos duplikāti
- 
```SQL
SELECT * FROM t_razotaji WHERE LOWER(razotajs) = LOWER(?);
```
- Ja nav atrasts ieraksts, tad tiks izveidots jauns ieraksts ražotāju tabulā un saglabāts id, lai pēc tam varētu izveidot jaunu ierakstu ar tikko izveidoto ražotāju
```SQL
INSERT INTO t_razotaji (razotajs) VALUES (?);
SELECT * FROM t_razotaji WHERE razotajs = ?
```
Ar nākošo vaicājumu, kur '?' vietā tiks ievietoti mainīgie, tiks izveidota jauna rinda tabulā t_vienumi
```SQL
INSERT INTO t_vienumi (svitr_kods,vienum_nosauk,modelis,razot_id,iss_aprakst,detalas,kateg_id,biroj_id,liet_id,bilde_cels,nopirkt_dat) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```
Parādīt informācīju par kādu vienu vienumu
```SQL
SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                   r.razotajs, iss_aprakst, detalas, komentars,
                   k.kategorija, b.birojs, l.lietv, bilde_cels,
                   v.nopirkt_dat, v.izveid_dat, v.atjauninats
                   FROM t_vienumi v
                   LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                   LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                   LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                   LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                   WHERE v.vienum_id = ?
```
Lai redigētu ierakstus datubāzē
```SQL
UPDATE t_vienumi
                       SET vienum_nosauk = ?, modelis = ?, razot_id = ?,
                       iss_aprakst = ?, detalas = ?, kateg_id = ?,
                       biroj_id = ?, liet_id = ?, bilde_cels = ?,
                       nopirkt_dat = ?, atjauninats = ? WHERE vienum_id = ?
```



