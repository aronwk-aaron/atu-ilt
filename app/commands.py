import click
import json
import pandas
from flatten_json import flatten
from flask.cli import with_appcontext
import datetime
from flask_user import current_app
from app import db
from app.models import Role, User, site, survey_species_camera
from app.schemas import siteSchema


@click.command("init_db")
@with_appcontext
def init_db():
    """ Initialize the database."""

    # print('Initializing Database.')
    # print('Dropping all tables.')
    # db.drop_all()
    # print('Creating all tables.')
    # db.create_all()
    # print('Database has been initialized.')
    return


@click.command("init_users")
@with_appcontext
def init_users():
    """ Initialize the users."""

    print('Creating Roles.')
    admin_role = find_or_create_role('admin')  # 1
    user_role = find_or_create_role('user')  # 2

    # Add users
    print('Creating Admin User.')
    admin_user = find_or_create_user(u'First', u'Last', u'example@example.com', 'Nope', admin_role)

    # Save to DB
    db.session.commit()
    return


def find_or_create_role(name):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

@click.command("fix_times")
@with_appcontext
def fix_times():
    '''
        Fix recoreded times
        where start is end and start
        is the same.
        Should only be used once really
    '''

    species_camera_times = survey_species_camera.query.all()
    fix_count = 0
    for item in species_camera_times:
        if item.start == item.end:
            fix_count += 1
            item.end = (item.end + datetime.timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S')
            item.save()
        item.start = (item.start + datetime.timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S')
        item.end = (item.end + datetime.timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S')
        item.save()
    print(f"Fixed: {fix_count} entries")
    return


@click.command("export_csv")
@with_appcontext
def export_csv():
    """ Genetate CVS report of all sites and surveys"""
    site_schema = siteSchema()
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).all(), many=True
        ).data
    )
    # pure jank
    df = pandas.json_normalize([flatten(site) for site in sites])

    df.to_csv('test.csv', index=False, encoding='utf-8')
    return
