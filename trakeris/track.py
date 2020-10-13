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
                   r.razotajs, iss_aprakst, detalas, komentars,
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
                   r.razotajs, iss_aprakst, detalas, komentars,
                   k.kategorija, b.birojs, l.lietv, bilde_cels,
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

        svitr_kods = db.execute(
                    '''SELECT MAX(svitr_kods)+1 AS lielakais_cip
                    FROM t_vienumi'''
        ).fetchone()

        # Values to get
        # biroj_id
        # kateg_id
        # razot_id

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

        if razot_id is None:
            db.execute(
            '''INSERT INTO t_razotaji (razotajs) VALUES (?)''',
            (razotajs,))
            db.commit()

            razot_id = db.execute(
                        '''SELECT * FROM t_razotaji WHERE razotajs = ?''',
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
            db.execute(
                    '''INSERT INTO t_vienumi (
                                   svitr_kods,vienum_nosauk,modelis,razot_id,
                                   iss_aprakst,detalas,kateg_id,
                                   biroj_id,liet_id,bilde_cels,nopirkt_dat)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (svitr_kods['lielakais_cip'],vienum_nosauk, modelis,
                    razot_id['razot_id'],iss_aprakst,detalas,
                    kateg_id['kateg_id'],biroj_id['biroj_id'],
                    g.user['liet_id'],filename,nopirkt_dat,)
            )
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

    return render_template("track/view.html", item=item)


@bp.route("/<int:item_id>/edit", methods=("GET", "POST"))
@login_required
def edit(item_id):
    db = get_db()
    item = get_item(item_id)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        vienum_nosauk = request.form['vienum_nosauk']
        birojs = request.form['birojs']
        kategorija = request.form['kategorija']
        nopirkt_dat = request.form['nopirkt_dat']
        iss_aprakst = request.form['iss_aprakst']
        razotajs = request.form['razotajs']
        modelis = request.form['modelis']
        detalas = request.form['detalas']

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

        liet_id = db.execute(
                    '''SELECT liet_id FROM t_lietotaji WHERE LOWER(lietv) = LOWER(?)''',
                    (lietv,)
        ).fetchone()

        print("lietotajs: %s" % lietv)



        if razot_id is None:
            db.execute(
            '''INSERT INTO t_razotaji (razotajs) VALUES (?)''',
            (razotajs,))
            db.commit()

            razot_id = db.execute(
                        '''SELECT * FROM t_razotaji WHERE razotajs = ?''',
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
            db.execute(
                    '''UPDATE t_vienumi
                       SET vienum_nosauk = ?, modelis = ?, razot_id = ?,
                       iss_aprakst = ?, detalas = ?, kateg_id = ?,
                       biroj_id = ?, liet_id = ?, bilde_cels = ?,
                       nopirkt_dat = ?, atjauninats = ? WHERE vienum_id = ?''',
                    (vienum_nosauk, modelis, razot_id['razot_id'],iss_aprakst,
                    detalas,kateg_id['kateg_id'],biroj_id['biroj_id'],
                    liet_id['liet_id'],filename,nopirkt_dat,timestamp,item_id)
            )
            db.commit()
            return redirect(url_for("track.index"))

    return render_template("track/edit.html", item=item, timestamp=timestamp,
                            t_kategorijas=t_kategorijas, t_biroji=t_biroji,
                            t_razotaji=t_razotaji, t_lietotaji=t_lietotaji,
                            today_date=today_date)
