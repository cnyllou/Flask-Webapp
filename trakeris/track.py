import time, functools, os
from datetime import datetime, date

from flask import Blueprint, flash
from flask import g, request, session
from flask import redirect, render_template, url_for
from flask import send_from_directory, current_app

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from trakeris.auth import login_required, allowed_file
from trakeris.db import get_db


bp = Blueprint('track', __name__)


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
                '''SELECT k.koment_id, k.komentars,
                   v.vienum_nosauk, l.lietv, k.noris_laiks
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
            flash('Request.files: '+ request.files)

        file = request.files['bilde_cels']

        if file.filename == '':
            flash('No selected file... Using default.')
        if file and allowed_file(file.filename):
            filename = ("{}_{}".format(
                                svitr_kods['lielakais_cip'],
                                secure_filename(file.filename)
                                )
                        )
            file.save(os.path.join(
                      current_app.config['ITEM_IMGAES'],
                      filename))
            flash("File saved in: " +
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

    t_vienumi = db.execute('''SELECT * FROM t_vienumi''').fetchone()

    for value in t_vienumi:
        # Create new array with all values
        # Compare this array with the updated one
        # Update history based on this logic
        flash("Type: '{}' - Value: '{}'".format(type("t_vienumi"), value))

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


@bp.route("/<int:item_id>/edit", methods=("GET", "POST"))
@login_required
def edit(item_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    item = get_item(item_id)
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

    t_lietotaji = db.execute(
                 '''SELECT liet_id, lietv
                    FROM t_lietotaji'''
    ).fetchall()


    if request.method == 'POST':
        lietv = request.form['lietv'] # Rule for it
        print("lietv: [{}]".format(lietv))
        vienum_nosauk = request.form['vienum_nosauk']
        birojs = request.form['birojs']
        kategorija = request.form['kategorija']
        nopirkt_dat = request.form['nopirkt_dat']
        iss_aprakst = request.form['iss_aprakst']
        razotajs = request.form['razotajs']
        modelis = request.form['modelis']
        detalas = request.form['detalas']
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

        if lietv is not "":
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
            flash("File saved in: " +
                  current_app.config['ITEM_IMGAES'] +
                  filename)

        print("file: " + str(filename))
        error = None

        if vienum_nosauk is None:
            error = "Nosaukums ir obligāts."
        elif birojs is None:
            error = "Atrašanās vieta ir obligāta."
        elif kategorija is None:
            error = "Kategorija ir obligāta."

        if error is not None:
            flash(error)
        #else:
            #t_vienumi = db.execute

            db.execute('''UPDATE t_vienumi
                          SET vienum_nosauk = ?, modelis = ?, razot_id = ?,
                          iss_aprakst = ?, detalas = ?, kateg_id = ?,
                          biroj_id = ?, liet_id = ?, bilde_cels = ?,
                          nopirkt_dat = ?, atjauninats = ? WHERE vienum_id = ?''',
                      (vienum_nosauk, modelis, razot_id['razot_id'],iss_aprakst,
                      detalas,kateg_id['kateg_id'],biroj_id['biroj_id'],
                      liet_id['liet_id'],filename['bilde_cels'],
                      nopirkt_dat,timestamp,item_id,))

            if liet_id['liet_id'] is "":
                update_history(item_id, session.get('user_id'), 4)
            elif liet_id['liet_id'] == session.get('user_id'):
                update_history(item_id, session.get('user_id'), 3)

            update_history(item_id, session.get('user_id'), darb_id)

            db.commit()
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')
    darb_id = 3

    flash("item={}, user={}".format(item_id, user_id))
    db = get_db()
    db.execute('''UPDATE t_vienumi
                  SET liet_id = ?,
                  atjauninats = ?
                  WHERE vienum_id = ?''',
              (user_id, timestamp, item_id))

    update_history(item_id, user_id, darb_id)
    db.commit()

    return redirect(url_for("track.index"))
