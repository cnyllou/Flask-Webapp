import time, functools, os
import pytz
from datetime import datetime, date
import pandas as pd

from flask import Blueprint, flash
from flask import g, request, session
from flask import redirect, render_template, url_for
from flask import send_from_directory, current_app

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from trakeris.auth import login_required, admin_required, allowed_file
from trakeris.db import get_db, backup_db


bp = Blueprint('track', __name__)
TIMEZONE = pytz.timezone('Europe/Riga')

@bp.route("/")
@login_required
def index():
    user_id = session.get('user_id')
    db = get_db()

    t_vienumi = db.execute(
                '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                   r.razotajs, iss_aprakst, detalas,
                   k.kateg_id, k.kategorija, b.biroj_id, b.birojs,
                   l.liet_id, l.lietv, bilde_cels, atjauninats
                   FROM t_vienumi v
                   LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                   LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                   LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                   LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                   ORDER BY atjauninats DESC'''
    ).fetchall()

    return render_template('track/index.html',
                            user_id=user_id,t_vienumi=t_vienumi)


def get_item(item_id):
    db = get_db()
    item = db.execute(
                '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                   r.razotajs, iss_aprakst, detalas,
                   k.kategorija, b.birojs, l.liet_id, l.lietv, bilde_cels,
                   v.nopirkt_dat, v.izveid_dat, v.atjauninats
                   FROM t_vienumi v
                   LEFT JOIN t_razotaji r ON v.razot_id = r.razot_id
                   LEFT JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                   LEFT JOIN t_biroji b ON v.biroj_id = b.biroj_id
                   LEFT JOIN t_lietotaji l ON v.liet_id = l.liet_id
                   WHERE v.vienum_id = ?''',
                   (item_id,),
    ).fetchone()

    if item is None:
        abort(404, "Item id {0} doesn't exist.".format(item_id))

    return item


def get_comments(item_id):
    db = get_db()
    comments = db.execute(
                '''SELECT koment_id, k.komentars,
                   v.vienum_nosauk, l.lietv, noris_laiks
                   FROM t_komentari k
                   JOIN t_vienumi v ON k.vienum_id = v.vienum_id
                   JOIN t_lietotaji l ON k.liet_id = l.liet_id
                   WHERE v.vienum_id = ?''',
                   (item_id,),
    ).fetchall()

    return comments


def get_history(item_id):
    db = get_db()
    history = db.execute(
                '''SELECT i.ierakst_id, v.vienum_nosauk, l.lietv,
                          d.darbiba, i.noris_laiks
                   FROM t_ieraksti i
                   JOIN t_vienumi v ON i.vienum_id = v.vienum_id
                   JOIN t_lietotaji l ON i.liet_id = l.liet_id
                   JOIN t_darbibas d ON i.darb_id = d.darb_id
                   WHERE v.vienum_id = ?''',
                   (item_id,),
    ).fetchall()

    return history


def get_table(table):
    db = get_db()

    query = "SELECT * FROM {}".format(table)
    #columns = db.execute("SELECT * FROM {}".format(table)).fetchall()

    df = pd.read_sql_query(query, db)

    return df


def get_all_tables():
    db = get_db()
    all_tables = ["t_lietotaji",
                  "t_biroji",
                  "t_pilsetas",
                  "t_projekti",
                  "t_pozicijas",
                  "t_vienumi",
                  "t_ieraksti",
                  "t_komentari",
                  "t_darbibas",
                  "t_kategorijas",
                  "t_razotaji"]
    combined_html = []

    for table in all_tables:
        print(">> Table: {}".format(table))
        query = "SELECT * FROM {}".format(table)
        df = pd.read_sql_query(query, db)

        combined_html.append(str(df.to_html(index=False)))


    return " ".join(combined_html)


def export_tables():
    timestamp = datetime.now(tz=TIMEZONE).strftime("%Y%m%d.%H%M%S")
    db = get_db()
    all_tables = ["t_lietotaji",
                  "t_biroji",
                  "t_pilsetas",
                  "t_projekti",
                  "t_pozicijas",
                  "t_vienumi",
                  "t_ieraksti",
                  "t_komentari",
                  "t_darbibas",
                  "t_kategorijas",
                  "t_razotaji"]

    directory_name = "backup_" + timestamp
    directory = os.path.join(current_app.config['BACKUP_FOLDER'],
                             directory_name)
    os.mkdir(directory)
    print(directory)

    for table in all_tables:
        print(">> Table: {}".format(table))
        query = "SELECT * FROM {}".format(table)
        filename = "{}_{}.csv".format(timestamp, table)
        file_path = os.path.join(directory, filename)

        df = pd.read_sql_query(query, db)
        csv = df.to_csv(index=False)

        print(csv)

        file = open(file_path, 'w', encoding="utf-16")
        file.write(csv)
        file.close()
        flash("File located at: {}".format(file_path))


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    db = get_db()
    today_date = date.today()

    t_biroji = db.execute(
                '''SELECT biroj_id, birojs
                   FROM t_biroji'''
    ).fetchall()

    t_kategorijas = db.execute(
                    '''SELECT kateg_id, kategorija
                       FROM t_kategorijas'''
    ).fetchall()

    t_razotaji = db.execute(
                 '''SELECT razot_id, razotajs
                    FROM t_razotaji'''
    ).fetchall()

    if request.method == 'POST':
        vienum_nosauk = request.form['vienum_nosauk']   # Obligāts
        birojs = request.form['birojs']                 # Obligāts
        kategorija = request.form['kategorija']         # Obligāts
        nopirkt_dat = request.form['nopirkt_dat']
        iss_aprakst = request.form['iss_aprakst']
        razotajs = request.form['razotajs']
        modelis = request.form['modelis']
        detalas = request.form['detalas']
        filename = 'default_item.png'
        darb_id = 1

        vienum_id = db.execute('''SELECT MAX(vienum_id)+1
                                  AS jaunakais_id
                                  FROM t_vienumi'''
        ).fetchone()
        jaunakais_id = vienum_id['jaunakais_id']

        svitr_kods = db.execute('''SELECT MAX(svitr_kods)+1
                                   AS lielakais_cip
                                   FROM t_vienumi'''
        ).fetchone()

        biroj_id = db.execute('''SELECT * FROM t_biroji
                                 WHERE birojs = ?''',
                             (birojs,)
        ).fetchone()

        kateg_id = db.execute('''SELECT * FROM t_kategorijas
                                 WHERE kategorija = ?''',
                             (kategorija,)
        ).fetchone()

        razot_id = db.execute('''SELECT * FROM t_razotaji
                                 WHERE LOWER(razotajs) = LOWER(?)''',
                             (razotajs,)
        ).fetchone()

        if razot_id is None:
            db.execute('''INSERT INTO t_razotaji (razotajs)
                          VALUES (?)''',
                      (razotajs,))
            db.commit()

            razot_id = db.execute('''SELECT * FROM t_razotaji
                                     WHERE razotajs = ?''',
                                 (razotajs,)
            ).fetchone()

        # check if the post request has the file part
        if 'bilde_cels' not in request.files:
            print('Request.files: '+ request.files)

        file = request.files['bilde_cels']

        if file.filename == '':
            print('No selected file... Using default.')
        if file and allowed_file(file.filename):
            filename = ("{}_{}".format(
                                svitr_kods['lielakais_cip'],
                                secure_filename(file.filename)
                                )
                        )
            file.save(os.path.join(
                      current_app.config['ITEM_IMGAES'],
                      filename))
            print("File saved in: " +
                  current_app.config['ITEM_IMGAES'] +
                  filename)

        error = None

        if vienum_nosauk is None:
            error = "Nosaukums ir obligāts."
        elif birojs is None:
            error = "Atrašanās vieta ir obligāta."
        elif kategorija is None:
            error = "Kategorija ir obligāta."

        if error is not None:
            flash(error)
        else:
            db.execute('''INSERT INTO t_vienumi (
                            svitr_kods,vienum_nosauk,modelis,razot_id,
                            iss_aprakst,detalas,kateg_id,
                            biroj_id,liet_id,bilde_cels,nopirkt_dat)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (svitr_kods['lielakais_cip'],vienum_nosauk, modelis,
                      razot_id['razot_id'],iss_aprakst,detalas,
                      kateg_id['kateg_id'],biroj_id['biroj_id'],
                      g.user['liet_id'],filename,nopirkt_dat,))

            update_history(jaunakais_id, g.user['liet_id'], darb_id)
            db.commit()

            return redirect(url_for("track.index"))

    return render_template('track/add.html', today_date=today_date,
                            t_kategorijas=t_kategorijas, t_biroji=t_biroji,
                            t_razotaji=t_razotaji)


@bp.route("/<int:item_id>/view", methods=("GET", "POST"))
@login_required
def view(item_id):
    db = get_db()
    item = get_item(item_id)
    comments = get_comments(item_id)
    history = get_history(item_id)

    if request.method == 'POST':
        komentars = request.form['komentars']
        liet_id = g.user['liet_id']
        error = None

        if komentars is None:
            error = "Komentārs ir tukšs"

        if error is not None:
            flash(error)
        else:
            db.execute('''INSERT INTO t_komentari(
                                      komentars,
                                      vienum_id,
                                      liet_id)
                          VALUES (?, ?, ?)''',
                          (komentars, item_id, liet_id,)
                      )
            db.commit()

            return redirect(url_for("track.view", item_id=item_id))

    return render_template("track/view.html",
                            item=item, comments=comments, history=history)


@bp.route("/tables", methods=("GET", "POST"))
@admin_required
def tables():
    if request.method == 'POST':
        timestamp = datetime.now(tz=TIMEZONE).strftime("%Y%m%d.%H%M%S")
        db = get_db()
        table = request.form['table']


        print(table)


        if table == "all":
            html = get_all_tables()

        elif table == "export_csv":
            export_tables()
            return render_template("track/tables.html")

        elif table == "backup":
            backup_db()
            return render_template("track/tables.html")

        else:
            df = get_table(table)

            html = df.to_html(index=False)

        filename = "tables/tabula-{}.html".format(table)
        full_path = os.path.join(current_app.config['REPORTING_FOLDER'],
                                 filename)
        file_path = os.path.join('trakeris/templates/',full_path)

        file = open(file_path, 'w', encoding="utf-16")
        file.write(html)
        file.close()
        flash("File located at: {}".format(os.path.abspath(full_path)))
        return render_template(full_path)


    return render_template("track/tables.html")


@bp.route("/queries", methods=("GET", "POST"))
@admin_required
def queries():
    db = get_db()

    return render_template("track/queries.html")


@bp.route("/reports", methods=("GET", "POST"))
@admin_required
def reports():
    db = get_db()

    return render_template("track/reports.html")

@bp.route("/<int:item_id>/edit", methods=("GET", "POST"))
@login_required
def edit(item_id):
    timestamp = datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    item = get_item(item_id)
    today_date = date.today()
    old_vienumi_array = []
    new_vienumi_array = []

    old_vienumi = db.execute('''SELECT liet_id, biroj_id, nopirkt_dat,
                                iss_aprakst, kateg_id, razot_id, vienum_nosauk,
                                modelis, bilde_cels, detalas
                                FROM t_vienumi
                                WHERE vienum_id = ?''',
                            (item_id,)).fetchone()

    for i, value in enumerate(old_vienumi):
        old_vienumi_array.append(value)
        print("old_value[{}]: '{}'".format(i, value))

    t_biroji = db.execute(
                '''SELECT biroj_id, birojs
                   FROM t_biroji'''
    ).fetchall()

    t_kategorijas = db.execute(
                    '''SELECT kateg_id, kategorija
                       FROM t_kategorijas'''
    ).fetchall()

    t_razotaji = db.execute(
                 '''SELECT razot_id, razotajs
                    FROM t_razotaji'''
    ).fetchall()

    t_lietotaji = db.execute(
                 '''SELECT liet_id, lietv
                    FROM t_lietotaji'''
    ).fetchall()


    if request.method == 'POST':
        print("--> POST Requested detected.")
        lietv = request.form['lietv'] # Rule for it
        print("--> lietv: [{}]".format(lietv))
        vienum_nosauk = request.form['vienum_nosauk']
        birojs = request.form['birojs']
        kategorija = request.form['kategorija']
        nopirkt_dat = request.form['nopirkt_dat']
        iss_aprakst = request.form['iss_aprakst']
        razotajs = request.form['razotajs']
        modelis = request.form['modelis']
        detalas = request.form['detalas']
        user_id = session.get('user_id')
        darb_id = 2

        svitr_kods = db.execute(
                    '''SELECT svitr_kods
                    FROM t_vienumi WHERE vienum_id = ?''',
                    (item_id,)
        ).fetchone()

        filename = db.execute(
                    '''SELECT bilde_cels FROM t_vienumi WHERE vienum_id = ?''',
                    (item_id,)
        ).fetchone()

        biroj_id = db.execute(
                    '''SELECT * FROM t_biroji WHERE birojs = ?''',
                    (birojs,)
        ).fetchone()

        kateg_id = db.execute(
                    '''SELECT * FROM t_kategorijas WHERE kategorija = ?''',
                    (kategorija,)
        ).fetchone()

        razot_id = db.execute(
                    '''SELECT * FROM t_razotaji WHERE LOWER(razotajs) = LOWER(?)''',
                    (razotajs,)
        ).fetchone()

        print("--> Data Fetched.")

        if lietv != "":
            liet_id = db.execute('''SELECT liet_id FROM t_lietotaji
                                    WHERE LOWER(lietv) = LOWER(?)''',
                                (lietv,)).fetchone()
        else:
            liet_id = {"liet_id": ""}

        if razot_id is None:
            db.execute('''INSERT INTO t_razotaji (razotajs)
                          VALUES (?)''',
                      (razotajs,))
            db.commit()

            razot_id = db.execute(
                        '''SELECT * FROM t_razotaji WHERE razotajs = ?''',
                        (razotajs,)
            ).fetchone()

        file = request.files['bilde_cels']

        if file and allowed_file(file.filename):
            filename = ("{}_{}".format(
                                svitr_kods['svitr_kods'],
                                secure_filename(file.filename)
                                )
                        )
            file.save(os.path.join(
                      current_app.config['ITEM_IMGAES'],
                      filename))
            print("File saved in: " +
                  current_app.config['ITEM_IMGAES'] +
                  filename)

        print("--> file: " + str(filename))
        error = None

        if vienum_nosauk is None:
            error = "Nosaukums ir obligāts."
        elif birojs is None:
            error = "Atrašanās vieta ir obligāta."
        elif kategorija is None:
            error = "Kategorija ir obligāta."

        if error is not None:
            flash(error)
        else:
            print("--> Error is None .")

            db.execute('''UPDATE t_vienumi
                          SET vienum_nosauk = ?, modelis = ?, razot_id = ?,
                          iss_aprakst = ?, detalas = ?, kateg_id = ?,
                          biroj_id = ?, liet_id = ?, bilde_cels = ?,
                          nopirkt_dat = ?, atjauninats = ? WHERE vienum_id = ?''',
                      (vienum_nosauk, modelis, razot_id['razot_id'],iss_aprakst,
                      detalas,kateg_id['kateg_id'],biroj_id['biroj_id'],
                      liet_id['liet_id'],filename['bilde_cels'],
                      nopirkt_dat,timestamp,item_id,))

            print("--> Query executed.")
            print("--> New vienumi starting...")
            new_vienumi = db.execute('''SELECT liet_id, biroj_id, nopirkt_dat,
                                        iss_aprakst, kateg_id, razot_id, vienum_nosauk,
                                        modelis, bilde_cels, detalas
                                        FROM t_vienumi
                                        WHERE vienum_id = ?''',
                                    (item_id,)).fetchone()

            print("--> New vienumi fetched.")
            for i, value in enumerate(new_vienumi):
                new_vienumi_array.append(value)
                print(" new_value[{}]: '{}'".format(i, value))

            array_change_before = list(set(old_vienumi_array) -
                                  set(new_vienumi_array))

            array_change_after = list(set(new_vienumi_array) -
                                 set(old_vienumi_array))

            array_changed_count = len(set(new_vienumi_array) -
                                  set(old_vienumi_array))

            if (array_change_before == []):
                array_change_before = array_change_before.append("")
                array_changed_count += 1
            elif (array_change_after == []):
                array_change_after = array_change_after.append("")
                array_changed_count += 1

            if (array_changed_count > 0):
                print("--> If changed 1 or 0 fulfilled.")
                if (
                        old_vienumi_array[0] == user_id and
                        new_vienumi_array[0] == ""
                   ):
                    print("--> User has returned the item.")
                    darb_id = 4
                elif new_vienumi_array[0] == user_id:
                    print("--> User has taken the item.")
                    darb_id = 3
                else:
                    print("--> Array before - {}.".format(old_vienumi_array[0]))
                    print(array_change_before)
                    print("--> Array after - {}.".format(new_vienumi_array[0]))
                    print(array_change_after)

                if (array_changed_count > 1):
                    update_history(item_id, user_id, 2)
                    print("--> Item was also editted.")

            print("--> Changed values({}) are - {}".
                  format(array_changed_count, array_change_after))

            update_history(item_id, user_id, darb_id)
            print("--> History table updated.")

            db.commit()
            print("--> Commit successfull.")

            return redirect(url_for("track.index"))

    return render_template("track/edit.html", item=item, timestamp=timestamp,
                            t_kategorijas=t_kategorijas, t_biroji=t_biroji,
                            t_razotaji=t_razotaji, t_lietotaji=t_lietotaji,
                            today_date=today_date)


def update_history(item_id, liet_id, darb_id):
    db = get_db()

    db.execute('''INSERT INTO t_ieraksti(vienum_id, liet_id, darb_id)
                        VALUES (?, ?, ?)''',
                        (item_id, liet_id, darb_id))


@bp.route("/addme/")
def addme():
    timestamp = datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')
    darb_id = 3

    print("item={}, user={}".format(item_id, user_id))
    db = get_db()
    db.execute('''UPDATE t_vienumi
                  SET liet_id = ?,
                  atjauninats = ?
                  WHERE vienum_id = ?''',
              (user_id, timestamp, item_id))

    update_history(item_id, user_id, darb_id)
    db.commit()

    return redirect(url_for("track.index"))
