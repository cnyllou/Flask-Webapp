---
title: Darāmais
created: '2020-10-01T18:50:39.295Z'
modified: '2020-10-07T17:04:40.824Z'
---

# Darāmais
## Priekšlapa
- [x] Navigāciju augšā ar logout labajā pusē
- [x] Kreisajā pusē galveno navigāciju ar izvēlēm
  - Virs visa ir lietotājs ar
    - profila bildi
    - Vārdu, Uzvārdu
    - Pozīciju
  - Viss inventārs
  - Pieprasīt inventāru
- [x] Ielogošanās lapa (Vienkārša paskata lapa)
  - E-pasts
  - Parole
- [ ] Galvenē var apskatīt visu inventāru
  - [ ] Filtru sadaļa
  - [ ] Meklēšanas lauks
  - [ ] Visi vienumi apskatāmi
    - Bildes (Ja nav tad, noklusējuma bilde)
    - Opcijas
      - Apskatīt
      - Rediģēt
    - Informācija
      - Nosaukums
      - Operētājsistēma
      - Atrašanās vieta
      - Kam piesaistīts
      - ID (XXXX)
- [ ] Administratora profils
  - Manto lietotāja izvēlni
  - Lietotāju pārvalde
- [ ] Lietotāju pārvalde
  - Administrators tikai var piekļūt
  - Iespējams:
    - Piereģistrēt, dzēst, modificēt lietotājus
    - Pievienot, dzēst, modificēt ierakstus inventāram

## Datubāzes daļa (Mini datubāze priekš mājaslapas būvēšanas)
- [x] - Lietotāji
  - ID, Vārds, Uzvārds, E-pasts, Parole, Pozīcija 
- [x] - Inventārs
  - ID, Kategorija, Ražotājs, Nosaukums, Modelis, 
  - bilde, Apraksts,
  - atrašanās vieta,  piesaistītais

## Prasības
- [ ] Reģistrācija notiek no administratora puses
  - Lietotājs ar administratora privilēģijām veido jaunu ierakstu datubāzē
- [x] Atverot mājaslapu parādas ielogošanās lapa
  - Vienkārša lapa ar tikai e-pastu un paroli
- [ ] Mājas lapā lietotājs var
  - Apskatīt visu invetāru
  - Apskatīt savu piesaistīto invetāru
  - Var filtrēt inventāru
  - Pievienot jaunu inventāru
  - Virspusēji redzēt savu informāciju
  - Izlogoties
- [ ] Administratora profils
  - Manto visu to, ko lietotājs var izdarīt
  - Var rediģēt, pievienot, dzēst darbiniekus no datubāzes
- [ ] Pievienot jaunu tehniku lapa
  - Jebkurš lietotājs var pievienot jaunu vienumu esošajam inventāram
