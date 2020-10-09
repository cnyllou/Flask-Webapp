import sqlite3
import csv, sys
import click

from flask import current_app, g
from flask.cli import with_appcontext

from trakeris.db import get_db


def import_csv(file_path):
    file = open(file_path, encoding="utf8")
    fileRead = csv.reader(file, delimiter='\t')
    fileData = list(fileRead)
    formatArray = []
    formatArrayRow = []

    print("Importē...")
    for row in fileData:
        print("> ", row)

    print("\nAtgriezt kā ir vai formatēt? (y, f)")
    a = input()
    if a == 'y':
        return fileData

    elif a == 'f':
        # print("List has ", len(fileData[0]), " elements")
        elc = len(fileData[0])
        if elc == 1:
            for i in fileData:
                i = ' '.join(map(str, i))
                formatArray.append(i)
        elif elc >= 2:
            for row in fileData:
                formatArrayRow = list(map(str.strip, row))
                formatArray.append(formatArrayRow)
    else:
        print("Atcelt atgriešanu.")

    return formatArray

# preces.csv table col1,col2
def instert_into_db(table, cols, data):
    col_count = len(cols.split(","))

    values_string = ", ?" * ((col_count) - 1)
    print()
    query = 'INSERT INTO {} ({}) VALUES (?{})'.format(
             table, cols, values_string)

    print("Tavs vaicājums:\n", query)
    print("Turpināt vai rediģēt? (r - rediģēt)")
    user_input = input()

    if user_input == 'r':
        print("\nIerakstiet savu vaicājumu:")
        new_query = input()
        print("Apstriprināt? (y, a - izmantot iepriekšējo, n - atcelt darbību)")
        user_input = input()
        if user_input == 'y':
            query = new_query
            print("Tiek izmantots vaicājums:\n" + query)
        elif user_input == 'a':
            print("Tiek izmantots vaicājums:\n" + query)
        else:
            raise "Programmas darbība tiek pārtraukta..."

    db = get_db()

    for row in data:
        if col_count == 1:
            values = row
        else:
            values = []
            for val in row:
                values.append(val)

        if col_count == 1:
            db.execute(query, [values])
            db.commit()
        else:
            db.execute(query, (values))
            db.commit()


    cursor = db.cursor()
    cursor.execute("SELECT * FROM {}".format(table))

    result = cursor.fetchall()

    for row in result:
        for field in row:
            print(field, end=" | ")
        print("")

@click.command('import-data')
@with_appcontext
def import_data_command():
    click.echo("IMPORT WIZARD ACTIVATED.")
    click.echo("Sintakse priekš importa ir sekojoša:")
    click.echo("datne tabula kol1,kol2,..,kol9")
    try:
        user_input = input()
        uargv = list(user_input.split(" "))
        try:
            filename = uargv[0]
            tablename = uargv[1]
            columns = uargv[2]

            print("Tavi parametri: ",uargv , "\n...\n")
            print("Dati no '{}' tiks importēti tabulas '{}' kolonās '{}'".
                  format(filename, tablename, columns))



        except IndexError as error:
            print("Error: ", error, "\nProgramma tiek slēgta.")

        import_data = import_csv(current_app.config['IMPORT_DATA'] + filename)

        # print("Import data:")
        # for x in import_data:
        #     print(x)

        instert_into_db(tablename, columns, import_data)


    except (NameError, OSError) as error:
        print("Error: ", error)


def init_app(app):
    app.cli.add_command(import_data_command)
