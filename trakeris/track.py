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

    user = db.execute(
        'SELECT * FROM t_lietotaji WHERE liet_id = ?', (user_id,)
    ).fetchone()

    filename = db.execute(
        'SELECT profil_bild_cels FROM t_lietotaji WHERE liet_id = ?', (user_id,)
    ).fetchone()

    t_vienumi = db.execute(
        "SELECT * FROM t_vienumi"
    ).fetchall()

    return render_template('track/index.html', user=user, t_vienumi=t_vienumi, filename=filename)


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
