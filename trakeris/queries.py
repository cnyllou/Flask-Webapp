import time, functools, os, pytz
import pandas as pd

from datetime import datetime, date
from flask import Blueprint, flash
from flask import g, request, session
from flask import redirect, render_template, url_for
from flask import send_from_directory, current_app

from trakeris.auth import login_required, admin_required, allowed_file
from trakeris.db import get_db

TABLE_STYLE = '''<style>
                    table {
                      border-collapse: collapse;
                      width: auto;
                    }

                    th, td {
                      text-align: left;
                      padding: 8px;
                    }

                    tr:nth-child(even){background-color: #f2f2f2}

                    th {
                      background-color: #6c5ce7;
                      color: white;
                    }
                </style>'''

# t_lietotaji
t_lietotaji = '''SELECT l.liet_id, lietv, parole, vards, uzv, poz.pozicija,
                        pro.projekts, b.birojs, pers_kods, epasts, tel_num,
                        profil_bild_cels
                  FROM t_lietotaji l
                       JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                       JOIN t_projekti pro ON l.proj_id = pro.proj_id
                       JOIN t_biroji b ON l.biroj_id = b.biroj_id'''

#t_biroji
t_biroji = '''SELECT biroj_id, birojs, p.pilseta
              FROM t_biroji b
                   JOIN t_pilsetas p ON b.pils_id = p.pils_id'''

#t_pilsetas
t_pilsetas = '''SELECT pilseta
              FROM t_pilsetas'''

t_kategorijas = '''SELECT kategorija FROM t_kategorijas'''

#t_vienumi
t_vienumi = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                        r.razotajs, iss_aprakst, detalas,
                        k.kategorija, b.birojs,
                        l.lietv, bilde_cels, atjauninats
                 FROM t_vienumi v
                      LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                      LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                      LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                      LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                 ORDER BY atjauninats DESC'''


vc_pilsetas = '''SELECT count(p.pilseta) AS 'Vienumu sk.', p.pilseta
               FROM t_vienumi v
               JOIN t_biroji b ON v.biroj_id = b.biroj_id
               JOIN t_pilsetas p ON b.pils_id = p.pils_id

               GROUP by p.pilseta
               ORDER BY count(p.pilseta) DESC
               '''

vc_birojs = '''SELECT count(b.birojs) AS 'Vienumu sk.', b.birojs
               FROM t_vienumi v
               LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
               GROUP by b.birojs
               ORDER BY count(b.birojs) DESC'''

vc_lietotaji = '''SELECT count(l.lietv) AS 'Vienumu sk.', l.lietv
               FROM t_vienumi v
                    LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
               GROUP by l.lietv
               ORDER BY count(l.lietv) DESC'''

vc_projekti = '''SELECT count(p.projekts) AS 'Vienumu sk.', p.projekts
               FROM t_vienumi v
                    LEFT JOIN t_projekti p ON v.liet_id = p.proj_id
               GROUP by p.projekts
               ORDER BY count(p.projekts) DESC'''

vc_pozicijas = '''SELECT count(poz.pozicija) AS 'Vienumu sk.', poz.pozicija
                  FROM t_vienumi v
                       JOIN t_lietotaji l ON v.liet_id = l.liet_id
                       JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                   GROUP by poz.pozicija
                   ORDER by count(poz.pozicija) DESC'''

vc_kategorijas = '''SELECT count(k.kategorija) AS 'Vienumu sk.', k.kategorija
                    FROM t_vienumi v
                         LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                    GROUP by k.kategorija
                    ORDER BY count(k.kategorija) DESC'''

vc_razotaji = '''SELECT count(r.razotajs) AS 'Vienumu sk.', r.razotajs
                 FROM t_vienumi v
                      LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                 GROUP by r.razotajs
                 ORDER BY count(r.razotajs) DESC'''

vg_pilsetas = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                        r.razotajs, iss_aprakst, detalas,
                        k.kategorija, b.birojs, p.pilseta,
                        l.lietv, bilde_cels, atjauninats
                 FROM t_vienumi v
                      LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                      LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                      LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                      LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                      LEFT JOIN t_pilsetas p ON b.pils_id = p.pils_id
              WHERE p.pilseta == '{}';
               '''

vg_biroji = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                        r.razotajs, iss_aprakst, detalas,
                        k.kategorija, b.birojs, p.pilseta,
                        l.lietv, bilde_cels, atjauninats
                 FROM t_vienumi v
                      LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                      LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                      LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                      LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                      LEFT JOIN t_pilsetas p ON b.pils_id = p.pils_id
              WHERE b.birojs == '{}';
               '''

vg_kategorijas = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                        r.razotajs, iss_aprakst, detalas,
                        k.kategorija, b.birojs, p.pilseta,
                        l.lietv, bilde_cels, atjauninats
                 FROM t_vienumi v
                      LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                      LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                      LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                      LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                      LEFT JOIN t_pilsetas p ON b.pils_id = p.pils_id
              WHERE k.kategorija == '{}';
               '''


#t_ieraksti
t_ieraksti = '''SELECT i.ierakst_id, v.vienum_nosauk, l.lietv, d.darbiba
                FROM t_ieraksti i
                     JOIN t_vienumi v ON i.vienum_id = v.vienum_id
                     JOIN t_lietotaji l ON i.liet_id = l.liet_id
                     JOIN t_darbibas d ON i.darb_id = d.darb_id'''

# t_komentari
t_komentari = '''SELECT koment_id, k.komentars,
                        v.vienum_nosauk, l.lietv, noris_laiks
                 FROM t_komentari k
                      JOIN t_vienumi v ON k.vienum_id = v.vienum_id
                      JOIN t_lietotaji l ON k.liet_id = l.liet_id'''

# Filtri
f_lietotaji_info = '''SELECT l.liet_id, lietv, parole, vards, uzv, poz.pozicija,
                        pro.projekts, b.birojs, pers_kods, epasts, tel_num,
                        profil_bild_cels
                  FROM t_lietotaji l
                       JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                       JOIN t_projekti pro ON l.proj_id = pro.proj_id
                       JOIN t_biroji b ON l.biroj_id = b.biroj_id
                  WHERE lietv == '{}';'''

f_lietotaji_vienumi = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                                r.razotajs, iss_aprakst, detalas,
                                k.kategorija, b.birojs,
                                l.lietv, bilde_cels, atjauninats
                         FROM t_vienumi v
                              LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                              LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                              LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                              LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                         WHERE lietv == '{}';'''

f_lietotaji_ieraksti = '''SELECT i.ierakst_id, v.vienum_nosauk, l.lietv, d.darbiba
                FROM t_ieraksti i
                     JOIN t_vienumi v ON i.vienum_id = v.vienum_id
                     JOIN t_lietotaji l ON i.liet_id = l.liet_id
                     JOIN t_darbibas d ON i.darb_id = d.darb_id
                WHERE lietv == '{}';'''

f_lietotaji_komentari = '''SELECT koment_id, k.komentars,
                        v.vienum_nosauk, l.lietv, noris_laiks
                 FROM t_komentari k
                      JOIN t_vienumi v ON k.vienum_id = v.vienum_id
                      JOIN t_lietotaji l ON k.liet_id = l.liet_id
                 WHERE lietv == '{}';'''

f_projekti_darbinieki = '''SELECT l.liet_id, lietv, parole, vards, uzv, poz.pozicija,
                        pro.projekts, b.birojs, pers_kods, epasts, tel_num,
                        profil_bild_cels
                  FROM t_lietotaji l
                       JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                       JOIN t_projekti pro ON l.proj_id = pro.proj_id
                       JOIN t_biroji b ON l.biroj_id = b.biroj_id
                  WHERE pro.projekts == '{}';'''

f_projekti_vienumi = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                                r.razotajs, iss_aprakst, detalas,
                                k.kategorija, b.birojs, p.projekts,
                                l.lietv, bilde_cels, atjauninats
                         FROM t_vienumi v
                              LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                              LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                              LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                              LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                              LEFT JOIN t_projekti p ON v.liet_id = p.proj_id
                         WHERE p.projekts == '{}';'''

f_razotaji_vienumi = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                                r.razotajs, iss_aprakst, detalas,
                                k.kategorija, b.birojs, p.projekts,
                                l.lietv, bilde_cels, atjauninats
                         FROM t_vienumi v
                              LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                              LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                              LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                              LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                              LEFT JOIN t_projekti p ON v.liet_id = p.proj_id
                         WHERE r.razotajs == '{}';'''

f_biroji_vienumi = '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                                r.razotajs, iss_aprakst, detalas,
                                k.kategorija, b.birojs, p.projekts,
                                l.lietv, bilde_cels, atjauninats
                         FROM t_vienumi v
                              LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                              LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                              LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                              LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                              LEFT JOIN t_projekti p ON v.liet_id = p.proj_id
                         WHERE b.birojs == '{}';'''

f_biroji_darbinieki = '''SELECT l.liet_id, lietv, parole, vards, uzv, poz.pozicija,
                        pro.projekts, b.birojs, pers_kods, epasts, tel_num,
                        profil_bild_cels
                  FROM t_lietotaji l
                       JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                       JOIN t_projekti pro ON l.proj_id = pro.proj_id
                       JOIN t_biroji b ON l.biroj_id = b.biroj_id
                  WHERE b.birojs == '{}';'''


def choose_query(query_name, f_lietotaji=None, f_projekti=None, f_razotaji=None, f_birojs=None):
    db = get_db()
    if query_name == "t_lietotaji":
        query_name = t_lietotaji
    elif query_name == "t_biroji":
        query_name = t_biroji
    elif query_name == "t_vienumi":
        query_name = t_vienumi
    elif query_name == "vc_pilsetas":
        query_name = vc_pilsetas
    elif query_name == "vc_birojs":
        query_name = vc_birojs
    elif query_name == "vc_lietotaji":
        query_name = vc_lietotaji
    elif query_name == "vc_projekti":
        query_name = vc_projekti
    elif query_name == "vc_pozicijas":
        query_name = vc_pozicijas
    elif query_name == "vc_kategorijas":
        query_name = vc_kategorijas
    elif query_name == "vc_razotaji":
        query_name = vc_razotaji
    elif query_name == "vg_pilsetas":
        query_name = vg_pilsetas
    elif query_name == "vg_biroji":
        query_name = vg_biroji
    elif query_name == "vg_kategorijas":
        query_name = vg_kategorijas
    elif query_name == "t_ieraksti":
        query_name = t_ieraksti
    elif query_name == "t_komentari":
        query_name = t_komentari
    else:
        print("Unknown query: [{}]".format(query_name))

    return query_name


def get_query(query, f_lietotajs=None, f_projekts=None, f_razotajs=None, f_birojs=None):
    db = get_db()
    query_name = query
    query = choose_query(query)

    if query_name == "vg_pilsetas":
        query_array = []
        pilsetas = db.execute(t_pilsetas).fetchall()

        for pilseta in pilsetas:
            print(pilseta['pilseta'])
            df = pd.read_sql_query(vg_pilsetas.format(pilseta['pilseta']), db)
            html = df.to_html(index=False)
            query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format(pilseta['pilseta']))
            query_array.append(html)
        html = " ".join(query_array)
    elif query_name == "vg_biroji":
        query_array = []
        biroji = db.execute(t_biroji).fetchall()

        for birojs in biroji:
            print(birojs['birojs'])
            df = pd.read_sql_query(vg_biroji.format(birojs['birojs']), db)
            html = df.to_html(index=False)
            query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format(birojs['birojs']))
            query_array.append(html)
        html = " ".join(query_array)
    elif query_name == "vg_kategorijas":
        query_array = []
        kategorijas = db.execute(t_kategorijas).fetchall()

        for kategorija in kategorijas:
            print(kategorija['kategorija'])
            df = pd.read_sql_query(vg_kategorijas.format(kategorija['kategorija']), db)
            html = df.to_html(index=False)
            query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format(kategorija['kategorija']))
            query_array.append(html)
        html = " ".join(query_array)
    elif query_name == "f_lietotaji" and f_lietotajs != None:
        query_array = []

        df = pd.read_sql_query(f_lietotaji_info.format(f_lietotajs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Dati"))
        query_array.append(html)

        df = pd.read_sql_query(f_lietotaji_vienumi.format(f_lietotajs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Vienumi"))
        query_array.append(html)

        df = pd.read_sql_query(f_lietotaji_ieraksti.format(f_lietotajs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Ieraksti"))
        query_array.append(html)

        df = pd.read_sql_query(f_lietotaji_komentari.format(f_lietotajs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Komentāri"))
        query_array.append(html)

        html = " ".join(query_array)

    elif query_name == "f_projekti" and f_projekts != None:
        query_array = []

        df = pd.read_sql_query(f_projekti_vienumi.format(f_projekts), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Projekta vienumi"))
        query_array.append(html)

        df = pd.read_sql_query(f_projekti_darbinieki.format(f_projekts), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Projekta komanda"))
        query_array.append(html)

        html = " ".join(query_array)
    elif query_name == "f_razotaji" and f_razotajs != None:
        query_array = []

        df = pd.read_sql_query(f_razotaji_vienumi.format(f_razotajs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Ražotāja vienumi"))
        query_array.append(html)

        html = " ".join(query_array)

    elif query_name == "f_biroji" and f_birojs != None:
        query_array = []

        df = pd.read_sql_query(f_biroji_darbinieki.format(f_birojs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Darbinieki"))
        query_array.append(html)

        df = pd.read_sql_query(f_biroji_vienumi.format(f_birojs), db)
        html = df.to_html(index=False)
        query_array.append("<h1 style='font-size:72px; padding-bottom:0px;'>{}</h1>".format("Vienumi"))
        query_array.append(html)

        html = " ".join(query_array)
    else:
        df = pd.read_sql_query(query, db)
        html = df.to_html(index=False)

    html = TABLE_STYLE + "\n" + html

    filename = "queries/query-{}.html".format(query_name)
    full_path = os.path.join(current_app.config['REPORTING_FOLDER'],
                             filename)
    file_path = os.path.join('trakeris/templates/', full_path)

    file = open(file_path, 'w', encoding="utf-8", errors='ignore')
    file.write(html)
    file.close()
    flash("File located at: {}".format(os.path.abspath(full_path)))

    return full_path



# def query_all_tables():
#     db = get_db()
#     all_tables = ["t_lietotaji",
#                   "t_biroji",
#                   "t_pilsetas",
#                   "t_projekti",
#                   "t_pozicijas",
#                   "t_vienumi",
#                   "t_ieraksti",
#                   "t_komentari",
#                   "t_darbibas",
#                   "t_kategorijas",
#                   "t_razotaji"]
#     combined_html = []
#
#     for table in all_tables:
#         print(">> Table: {}".format(table))
#         query = "SELECT * FROM {}".format(table)
#         df = pd.read_sql_query(query, db)
#
#         combined_html.append(str(df.to_html(index=False)))
#
#
#     return " ".join(combined_html)
#
