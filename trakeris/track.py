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
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    items = db.execute(
        "SELECT * FROM items"
    ).fetchall()

    return render_template('track/index.html', user=user, items=items)


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_cat = request.form['item_cat']
        error = None

        if item_name is None:
            error = "Nosaukums ir obligāts."
        elif item_cat is None:
            error = "Kategorija ir obligāts."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO items (item, category) VALUES (?, ?)',
                (item_name, item_cat)
            )
            db.commit()
            return redirect(url_for("track.index"))

    return render_template('track/add.html')
