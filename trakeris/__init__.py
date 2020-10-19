import os

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'trakeris.sqlite'),
        DATABASE_NAME='trakeris',

        IMPORT_DATA='trakeris/import_data/tabulas_excel/',
        REPORTING_FOLDER='track/reporting/',
        BACKUP_FOLDER='trakeris/backups/',

        UPLOAD_FOLDER = 'trakeris/static/images/profile_pics/',
        ITEM_IMGAES='trakeris/static/images/item_pics/'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    # Register the database commands
    from trakeris import db

    db.init_app(app)

    # My own custom script
    from trakeris import import_data

    import_data.init_app(app)

    # Pielietot Blueprint lietotnei
    from trakeris import auth, track

    app.register_blueprint(auth.bp)
    app.register_blueprint(track.bp)

    # Pārvirzīt lietotāju uz galveno lapu
    app.add_url_rule("/", endpoint='index')

    return app
