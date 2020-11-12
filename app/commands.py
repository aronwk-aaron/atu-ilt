import click
from flask.cli import with_appcontext
import datetime
from flask_user import current_app
from app import db
from app.models import Role, User


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