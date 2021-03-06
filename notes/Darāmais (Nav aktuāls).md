---
tags: [Base, To Do]
title: Darāmais (Nav aktuāls)
created: '2020-10-01T18:50:39.295Z'
modified: '2020-10-20T08:26:56.783Z'
---

# Darāmais (Nav aktuāls)
## Priekšlapa
- [x] Navigāciju augšā ar logout labajā pusē
- [x] Kreisajā pusē galveno navigāciju ar izvēlēm
  - Virs visa ir lietotājs ar
    - profila bildi
    - Vārdu, Uzvārdu
    - Pozīciju
  - Viss inventārs
- [x] Ielogošanās lapa (Vienkārša paskata lapa)
  - Lietotājvārds
      - burti tiek pārvērsti uz mazajiem
  - Parole
- [ ] Galvenē var apskatīt visu inventāru
  - [ ] Filtru sadaļa
  - [ ] Meklēšanas lauks
  - [x] Viss inventārs ir virspusēji apskatāms
      - Bilde
      - Nosaukums
      - Komentārs
      - Atrašanās vieta
      - Kam piesaistīts
      - Vienuma ID
      - Vienumam mainas krāsa balstoties uz statusu
  - [ ] Visus vienumus var sīkāk apskatīt
      - [ ] Uznirstošās iespējas
          - Apskatīt
              - [ ] Pa virsu uzlecas logs ar detalizētu informāciju par vienumu
              - [ ] Var ierakstīt komentārus
              - [ ] Var apskatīt ierakstu vēsturi
          - Rediģēt (Vēlāk atlikt)
          - Piesaistīt man
- [x] Inventāra papildināšana
    - Automātiski uzģenerājas unikāls svītrkods
    - [x] Obligātie lauki
        - Atrašanās vieta
        - Atbildīgais
        - Nosaukums
        - Kategorija
    - [x] neobligātie lauki
        - Pirkšanas datums
        - Īss apraksts
        - Ražotājs
            - Automātiskie piedāvājumi
            - Ja nav ievadītais sarakstā, tad tiek veidots jauns ieraksts t_razotaji
        - Modelis
        - Bilde
        - Detaļas
- [ ] Administratora profils
  - Manto lietotāja izvēlni
  - Lietotāju pārvalde
- [ ] Lietotāju pārvalde
  - Administrators tikai var piekļūt
  - Iespējams:
    - Piereģistrēt, dzēst, modificēt lietotājus
    - Pievienot, dzēst, modificēt ierakstus inventāram
- [ ] Validācijas
    - [ ] Reģistrācija
        - lietotājvārds tiek pārveidots uz mazajiem burtiem
        - Vārds, Uzvārds - vienmēr pārvēršas ar pirmo lielo burtu
        - Pārbaudīt pareizos datu tipus
        - Pārbaudīt datu tipu pie bildes augšupielādes
        - E-pasts
    - [ ] Ielogošanās
        - lietotājvārds tiek pārveidots uz mazajiem burtiem
    - [ ] Vienumi
        - [x] Pievienošana
            - Pirkšanas datumu nevar ievadīt lielāku par šodienu
            - Pārbaudīt datu tipu pie bildes augšupielādes
            - Lielie un mazie burti
            - Vienums parādas pats pirmais sarakstā
        - [ ] Rediģēšana
            - Pārbaudīt datu tipu pie bildes augšupielādes

## Datubāzes iesākšana (Minimāla datubāze priekš mājaslapas pamata funkcionalitātes)
- [x] - Lietotāji
  - ID, Vārds, Uzvārds, E-pasts, Parole, Pozīcija 
- [x] - Inventārs
  - ID, Kategorija, Ražotājs, Nosaukums, Modelis, 
  - bilde, Apraksts,
  - atrašanās vieta,  piesaistītais

## Datubāzes pilnveidošana
- [ ] Sasaistīt datus ar saitēm
- [ ] t_pilsetas
    - pils_id,pilseta
- [ ] t_projekti
    - proj_id,projekts
- [ ] t_pozicijas
    - poz_id,pozicija
- [ ] t_darbibas 
    - darb_id,darbiba
- [ ] t_kategorijas 
    - kateg_id,kategorija
- [ ] t_razotaji 
    - razot_id,razotajs
    - Lauku var aizpildīt lietotājs, ja neatrod sarakstā
- [ ] t_statusi 
    - stat_id,status
- [ ] t_lietotaji
    - liet_id,lietv,parole,vards,uzv,poz_id,proj_id,biroj_id,pers_kods,epasts,tel_num,profil_bild_cels
- [ ] t_biroji
    - biroj_id,birojs,pils_id
- [ ] t_vienumi
    - vienum_id,svitr_kods,vienum_nosauk,modelis,razot_id,iss_aprakst,detalas,komentars,kateg_id,biroj_id,liet_id,bilde_cels,nopirkt_dat
    - [ ] Atbildīgais lietotājs
- [ ] t_ieraksti
    - ierakst_id,vienum_id,liet_id,darb_id


## Prasības
- [ ] Reģistrācija 
    - Obligātie aizpildāmie lauku
        - parole, vārds, uzvārds, personas kodas,
        - pozīcija, projekts, birojs
        - e-pasts, telefona numurs
    - Neobligāti aizpildāmie lauku
        - Lietotājvārds
            - Ja lietotājvārds netiek dots, tas tiek automātiski ģenerēts
        - Profila bilde
    - Validācijas
        - personas kods un telefona numurs 
            - jābūt pareizi formatētai ievadei
- [x] Atverot mājaslapu parādas pieteikšanās lapa
    - Pieteikšanās ar lietotājvārdu un paroli
- [ ] Mājas lapā lietotājs var
    - Apskatīt visu invetāru
        - Sīkāk apskatīt (komentāri, detalizēti info, darbību ieraksti)
        - Vienumam mainas krāsa balstoties uz statusu
    - Rediģēt inventāru
        - Detaļas
        - Īsu aprakstu
        - Nosaukumu
    - Apskatīt savu piesaistīto invetāru
    - Var filtrēt inventāru pēc
        - Kategorijas
        - Atrašanās vietas
        - Statusa
        - Noņemt filtrus poga
    - Pievienot jaunu inventāru
    - Virspusēji redzēt savu informāciju
        - Vārds, uzvārds, profila bilde, pozīcija
    - Izlogoties
- [ ] Lietotāja profils
    - Lietotājs var rediģēt savu informāciju
        - projekts, pozīcija
- [ ] Administratora profils
    - Manto visu to, ko lietotājs var izdarīt
    - Var rediģēt, pievienot, dzēst darbiniekus no datubāzes
- [ ] Inventāra sadaļa
    - Katram vienumam automātiski piesaistas klase
        - kategorija - kategorijas ID
        - birojs - biroja ID
        - status
            - Pēc koda tiek noteikts status
                - Aizņemts, Man piesaistīts, Pieejams

# Darāmais saraksts
- [x] - Rediģēt reģistrācijas lapu priekš esošās datubāzes
- [x] - Ieteikumi priekš ražotājiem
- [x] - \<label> tags priekš formām
- [x] - Automātiska lietotājvārda ģenerēšana
- [ ] - Personas koda validācija
- [ ] - Telefona numura validācija
- [x] - Neļaut lietotājam reģistrēties kā administratoram
- [x] - Vārds, Uzvārds tiek ierakstīt ar pirmo lielo burtu neatkarīgi no lietotāja ievades
- [x] - Lietotāvārds tiek ierakstīts ar mazajiem burtiem neatkarīgi no lietotāja ievades
- [ ] - Profila bilde vienmēr vienā izmērā
- [x] - Filtri
- [x] - Izvēlētie filtri tiek atgriezti uz noklusējumu pēc lapas pārlādes
- [x] - Meklēšana
- [x] - Uznirstošās iespējas
- [ ] - Iespēja piesaistīt vienumu
- [x] - Iespēja sīkāk apskatīt vienumu
- [ ] - Iespēja rediģēt vienumu
- [x] - Atsevišķa lapa priekš rediģēšanas
- [ ] - Noklusējumā ir izvēlēta pareizā kategorija, birojs
- [x] - Atjaunināšanas laiks mainas pēc jauninājuma


# Problēmas
- [x] - Lietotājs nemainas
    - [x] Programmai kaut kas nepatik
- [ ] - NULL tiek ierakstīts komentāros
- [ ] - Pirkšanas datums ir tukšs

# Atlikt uz pašām beigām
- [ ] - Modal priekš rediģēšanas un apskatīšanas
- [ ] - Vienlaicīgs filtrs no meklēšanas un no kastītēm
- [ ] - Dizaina uzlabošana
- [ ] - Izvietošana serverī
- [ ] - Salabot, labo navigācijas pusi (Vai pārtaisīt visu navigācijas sadaļu)

