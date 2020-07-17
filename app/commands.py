import click
from flask.cli import with_appcontext
# import datetime
from app import db


@click.command("init_db")
@with_appcontext
def init_db():
    """ Initialize the database."""

    print('Initializing Database.')
    print('Dropping all tables.')
    db.drop_all()
    print('Creating all tables.')
    # db.create_all()
    print('Database has been initialized.')
