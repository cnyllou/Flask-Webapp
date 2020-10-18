import sqlite3, io, click, pytz, os

from datetime import datetime, date
from flask import current_app, g, flash
from flask.cli import with_appcontext

TIMEZONE = pytz.timezone('Europe/Riga')

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def backup_db():
    timestamp = datetime.now(tz=TIMEZONE).strftime("%Y%m%d.%H%M%S")
    db = get_db()
    database_name = current_app.config['DATABASE_NAME']

    backup_folder = os.path.join(current_app.config['BACKUP_FOLDER'], 'sqlite_database/')
    print(backup_folder)


    filename = "{}_{}_{}.sql".format(timestamp, database_name, "backup")
    file_path = os.path.join(backup_folder, filename)

    with io.open(file_path, 'w', encoding='utf-16') as f:
       for linha in db.iterdump():
           f.write('%s\n' % linha)
    print('Backup performed successfully.')
    flash('Datubāzes kopija saglabāta: {}'.format(file_path))
    db.close()


def init_db():
    db = get_db()


    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
