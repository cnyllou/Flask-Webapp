import sqlite3
import csv, sys
import click

from flask import current_app, g
from flask.cli import with_appcontext

from trakeris.db import get_db


def import_csv(file_path):
    file = open(file_path)
    fileRead = csv.reader(file)
    fileData = list(fileRead)
    formatArray = []
    formatArrayRow = []

    print("Importing...")
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
        print("Aborting return.")

    return formatArray

# preces.csv table col1,col2
def instert_into_db(table, cols, data):
    for row in data:
        values_string = ", ?" * ((len(row)) - 1)
        query = 'INSERT INTO {} ({}) VALUES (?{})'.format(
                 table, cols, values_string)

    print("Your query:\n", query)
    #db = get_db()

    #db.execute(query, )
    #db.commit()

@click.command('import-data')
@with_appcontext
def import_data_command():
    click.echo("IMPORT WIZARD ACTIVATED.")
    click.echo("Import syntax is the following:")
    click.echo("csv_filepath table col1,col2,..,col9")
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


    except NameError as error:
        print("Error: ", error)


def init_app(app):
    app.cli.add_command(import_data_command)
