from flask import Blueprint, flash
from flask import g, request, session
from flask import redirect, render_template, url_for
from werkzeug.exceptions import abort

from trakeris.auth import login_required
from trakeris.db import get_db


bp = Blueprint('track', __name__)


@bp.route("/")
@login_required
def index():
    user_id = session.get('user_id')
    db = get_db()

    t_lietotaji = db.execute(
                '''SELECT l.liet_id, vards, uzv, poz.pozicija, profil_bild_cels
                FROM t_lietotaji l
                JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                WHERE l.liet_id = ?''',
                (user_id,),
                ).fetchone()


    t_vienumi = db.execute(
                '''SELECT vienum_id, svitr_kods, vienum_nosauk, modelis,
                   r.razotajs, iss_aprakst, detalas, komentars,
                   k.kategorija, b.birojs, l.lietv, bilde_cels, nopirkt_dat
                   FROM t_vienumi v
                   JOIN t_razotaji r ON v.razot_id = r.razot_id
                   JOIN t_kategorijas k ON v.kateg_id = k.kateg_id
                   JOIN t_biroji b ON v.biroj_id = b.biroj_id
                   JOIN t_lietotaji l ON v.liet_id = l.liet_id
                   ORDER BY nopirkt_dat DESC'''
    ).fetchall()




    return render_template('track/index.html',
                            t_lietotaji=t_lietotaji, t_vienumi=t_vienumi)


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    if request.method == 'POST':
        vienum_nosauk = request.form['vienum_nosauk']
        kateg_id = request.form['kateg_id']
        error = None

        if vienum_nosauk is None:
            error = "Nosaukums ir obligāts."
        elif kateg_id is None:
            error = "Kategorija ir obligāts."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO t_vienumi (item, category) VALUES (?, ?)',
                (vienum_nosauk, kateg_id)
            )
            db.commit()
            return redirect(url_for("track.index"))

    return render_template('track/add.html')
