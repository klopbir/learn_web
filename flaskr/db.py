"""
Every package in python has __init__.py file
that executes when its being imported and other files are executed only when imported in __init__.py
So sometimes although we imported a package we still have to write from package import this
Python does not load other modules


So at the end of __init__.py there should either be global app or global create_app
"""



import sqlite3
from datetime import datetime

import click
from flask import current_app,g


def get_db():
    if 'db' not in g:    # can do this in python #             # special object that stores data, saves connection to the database to be able to reuse it afterwards
        g.db = sqlite3.connect(current_app.config['DATABASE'], # since the Flask object is not global instead of it we can access configs or the app itself using current_app
                               detect_types=sqlite3.PARSE_DECLTYPES
                               )
                                                               # creates flaskr.sqlite
                                                               # they are both contextual objects
        g.db.row_factory = sqlite3.Row                         # sqlite3.Row wraps the tuples returned by db into an object that lets u access wth keys
                                                               # row_factory is a function to build rows, by default python makes them into tuples
                                                               # Every sqlite3.Connection object has an attribute row_factory like g.db
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))               # executes the command on db


@click.command('init-db')                                  # creates a cli command
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('say-hello')                                # u need this kind of decorator because u want your decorator to execute generate command line object
def say_hello():                                           # since init_db_command = click.command('init-db')(init_db_command) so init_db_command is now click.Command type object
    """Say hello to the user."""                           # but u can still call it since click.Command is callable object
                                                           # so click.command and the wrapper inside it is only responsible for generating click.Command object
                                                           # that is why u have to manually add it to cli list later
    click.echo(click.style('Hello, world!', fg='red'))
    print("Hello, world!")
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)             # when it calls the close_db it automatically removes the g from the context
                                                  # because each connection is a function length thing so call close_db
    app.cli.add_command(init_db_command)          # decorators are executed during module import and even at definition, not function call
                                                  # so init_db_command already points to decorated version
                                                  # init_db_command = click.command('init-db')(init_db_command)
                                                  # it calls click.command('init-db') which rets a func then defines init-db-command function
                                                  # then it uses that formula and init_db_command = wrapper(init_db_command)
                                                  # then adds cli string argument from parent function to the click.Command object and returns it

                                                  # Decorators run when the function is defined, not when the function is called
    app.cli.add_command(say_hello)                # say_hello is click.Command object so is used directly inside add_command


    # flask.exe is just wrapper for python code. It holds the location of the interpreter || and parent process of python does not stop until python
    # and then constructs a new command line string that includes the arguments you typed with python.exe
    # So u get something like this
    # CreateProcess("C:\Path\To\flask.exe", "--app flaskr init-db")
    # In shell: C:\path\to\python.exe "C:\path\to\Scripts\flask-script.py" --app flaskr init-db
    # ['C:\\...\\flask-script.py', '--app', 'flaskr', 'init-db']
    # Then python builds its sys.argv = ['flask-script.py', '--app', 'flaskr', 'init-db']

    # The code in flask-script.py
    # #!C:\Path\to\python.exe
    # # -*- coding: utf-8 -*-
    # import re
    # import sys
    # from flask.cli import main
    #
    # if __name__ == '__main__':
    #     sys.exit(main())
    # and it click uses sys.argv to get the options and then handles them
    # sys.argv is provided by the OS to the current process # it's just argv in C lang
    # ['flask', '--app', 'flaskr', 'init-db'] are process arguments