---
tags: [Datubāze, SQL]
title: SQL JOIN veidi
created: '2020-10-10T18:44:13.480Z'
modified: '2020-10-10T18:55:36.397Z'
---

# SQL JOIN veidi

## INNER JOIN
Sasaistot tabulas, vaicāju atgriež tikai rindas, kurās ir saistoši dati, ja nav tādu saistošu datu, tad nekas netiek atgriezts.

## LEFT JOIN
Īsumā ņemot tabulu A un tabulu B.
Vaicājums atgriež tabulu A un pievieno jebkurus saistošus datus no tabulas B.
- Ja nav saistoši dati, tad ierakstu vērtības tiek atgrieztas kā NULL.

## RIGHT JOIN
- Pretējais LEFT JOIN
Vaicājums atgriež tabulu B un pievieno jebkurus saistošu datus no tabulas A.

## FULL JOIN
Vaicājums atgriež datus no abām tabulām neatkarīgi vai tajos ir saistīti ieraksti, nesaistītiem ierakstiem kā iepriekš minētajos vērtība tiks uzrādīta kā NULL.
