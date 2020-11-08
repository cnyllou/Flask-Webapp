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


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['pozicija'] != 'Administrators':
            return redirect(url_for('track.index'))

        return view(**kwargs)
    return wrapped_view


@bp.route('../static/images/profile_pics/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@bp.route('/register', methods=('GET', 'POST'))
@admin_required
def register():
    db = get_db()

    t_pozicijas = db.execute(
                '''SELECT poz_id, pozicija
                   FROM t_pozicijas'''
    ).fetchall()

    t_projekti = db.execute(
                '''SELECT proj_id, projekts
                   FROM t_projekti'''
    ).fetchall()

    t_biroji = db.execute(
                '''SELECT biroj_id, birojs
                   FROM t_biroji'''
    ).fetchall()

    if request.method == 'POST':
        lietv = (request.form['lietv']).lower()
        parole = request.form['parole']
        vards = (request.form['vards']).capitalize()
        uzv = request.form['uzv'].capitalize()
        pozicija = request.form['pozicija']
        projekts = request.form['projekts']
        birojs = request.form['birojs']
        pers_kods = request.form['pers_kods']
        epasts = (request.form['epasts']).lower()
        tel_num = request.form['tel_num']
        filename = 'default.png'

        proj_id = db.execute(
                    '''SELECT * FROM t_projekti WHERE projekts = ?''',
                    (projekts,)
        ).fetchone()

        poz_id = db.execute(
                    '''SELECT * FROM t_pozicijas WHERE pozicija = ?''',
                    (pozicija,)
        ).fetchone()

        biroj_id = db.execute(
                    '''SELECT * FROM t_biroji WHERE birojs = ?''',
                    (birojs,)
        ).fetchone()

        # check if the post request has the file part
        if 'profil_bild_cels' not in request.files:
            flash('Request.files: '+ request.files)

        file = request.files['profil_bild_cels']
        # flash("File found: " + file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file... Using default.')
        if file and allowed_file(file.filename):
            filename = ("{}_{}".format(lietv, secure_filename(file.filename)))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash("File saved in: " + current_app.config['UPLOAD_FOLDER'] + filename)

        error = None

        if not lietv:
            # Ģenerēt lietotājvārdu
            lietv = ("{}.{}".format(vards, uzv)).lower()
            if db.execute(
                'SELECT liet_id FROM t_lietotaji WHERE LOWER(lietv) = LOWER(?)',
                (lietv,)
            ).fetchone() is not None:
                error = 'Lietotājs {} jau eksistē'.format(lietv)

        if not parole:
            error = 'Parole ir obligāta.'
        elif not vards:
            error = 'Vārds ir obligāts'
        elif not uzv:
            error = 'Uzvārds ir obligāts.'
        elif not pozicija:
            error = 'Pozīcija ir obligāta.'
        elif (pozicija).lower() == 'administrators':
            error = 'Jaunus administratorus var tikai piereģistrēt administrators'
        elif not projekts:
            error = 'Projekts ir obligāts.'
        elif not birojs:
            error = 'Birojs ir obligāts.'
        elif not pers_kods:
            error = 'Personas kods ir obligāts.'
        elif not epasts:
            error = 'E-pasts ir obligāts.'
        elif not tel_num:
            error = 'Telefona numurs ir obligāts.'
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
                 poz_id['poz_id'], proj_id['proj_id'], biroj_id['biroj_id'],
                 pers_kods, epasts, tel_num, filename)
            )
            db.commit()
            return redirect(url_for('track.index'))

        flash(error)

    return render_template('auth/register.html', t_pozicijas=t_pozicijas,
                            t_projekti=t_projekti, t_biroji=t_biroji)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        lietv = request.form['lietv']
        parole = request.form['parole']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT liet_id, lietv, parole FROM t_lietotaji WHERE lietv = ?', (lietv,)
        ).fetchone()
        if user is None:
            error = 'Nepareizs lietotājs vai parole.'
        elif not check_password_hash(user['parole'], parole):
            error = 'Nepareizs lietotājs vai parole.'

        if error is None:
            session.clear()
            session['user_id'] = user['liet_id']
            return redirect(url_for('track.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
                    '''SELECT l.liet_id, l.lietv, vards, uzv, poz.pozicija, profil_bild_cels
                    FROM t_lietotaji l
                    JOIN t_pozicijas poz ON l.poz_id = poz.poz_id
                    WHERE l.liet_id = ?''',
                    (user_id,),
                    ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
