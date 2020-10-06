import functools, os

from flask import Blueprint, flash
from flask import g, request, session
from flask import redirect, render_template, url_for
from flask import send_from_directory, current_app

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from trakeris.db import get_db

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('../static/images/profile_pics/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        lietv = request.form['lietv']
        parole = request.form['parole']
        vards = request.form['vards']
        uzv = request.form['uzv']
        poz_id = request.form['poz_id']
        proj_id = request.form['proj_id']
        biroj_id = request.form['biroj_id']
        pers_kods = request.form['pers_kods']
        epasts = request.form['epasts']
        tel_num = request.form['tel_num']
        filename = '../default.png'

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Request.files: '+ request.files)

        file = request.files['file']
        # flash("File found: " + file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file... Using default.')
        if file and allowed_file(file.filename):
            filename = ("{}_{}".format(lietv, secure_filename(file.filename)))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash("File saved in: " + current_app.config['UPLOAD_FOLDER'] + filename)

        db = get_db()
        error = None

        # Lietotāja ievades validēšana
        if not lietv:
            error = 'Ievadiet lietotāja vārdu.'
        elif not parole:
            error = 'Ievadiet paroli.'
        elif db.execute(
            'SELECT liet_id FROM t_lietotaji WHERE lietv = ?', (lietv,)
        ).fetchone() is not None:
            error = 'Lietotājs {} jau eksistē'.format(lietv)

        if error is None:
            db.execute(
                'INSERT INTO t_lietotaji (lietv, parole, vards, uzv,'
                ' poz_id, proj_id, biroj_id, pers_kods, epasts, tel_num, profil_bild_cels)'
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (lietv, generate_password_hash(parole), vards, uzv,
                 poz_id, proj_id, biroj_id, pers_kods, epasts, tel_num, filename)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        lietv = request.form['lietv']
        parole = request.form['parole']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM t_lietotaji WHERE lietv = ?', (lietv,)
        ).fetchone()
        flash(user['lietv'])

        if user is None:
            error = 'Nepareizs lietotajs.'
        elif not check_password_hash(user['parole'], parole):
            error = 'Nepareiza parole'

        if error is None:
            session.clear()
            session['user_id'] = user['liet_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM t_lietotaji WHERE liet_id = ?', (user_id,)
        ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
