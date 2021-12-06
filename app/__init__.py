import os
from flask import Flask
from flask_assets import Environment
from webassets import Bundle

from app.models import db, migrate
from app.schemas import ma
from flask_wtf.csrf import CSRFProtect

from app.commands import init_db, init_users, export_csv, fix_times
from app.models import User, Role, UsersRoles, UserInvitation
from flask_user import user_registered, UserManager


# Instantiate Flask extensions
csrf_protect = CSRFProtect()
# db and migrate is instantiated in models.py


def create_app():
    """Create and configure the Flask app

    Returns:
        Flask: the configured app
    """

    app = Flask(__name__, instance_relative_config=True)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings

    app.config['TESTING'] = False
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('APP_DATABASE_URI')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 2,
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_use_lifo": True
    }
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['USER_EMAIL_SENDER_NAME'] = os.getenv('USER_EMAIL_SENDER_NAME')
    app.config['USER_EMAIL_SENDER_EMAIL'] = os.getenv('USER_EMAIL_SENDER_EMAIL')

    def calc_datetime(value, stop):
        difference = stop - value
        return difference

    app.jinja_env.filters['time_delta'] = calc_datetime

    register_extensions(app)
    register_blueprints(app)
    # add the init_db command to flask cli
    # app.cli.add_command(init_db)
    app.cli.add_command(init_users)
    app.cli.add_command(export_csv)
    app.cli.add_command(fix_times)

    @user_registered.connect_via(app)
    def after_register_hook(sender, user, **extra):

        role = Role.query.filter_by(name="user").first()

        if role is None:
            role = Role(name="user")
            db.session.add(role)
            db.session.commit()

        user_role = UsersRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

    return app


def register_extensions(app):
    """Register extensions for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    db.init_app(app)
    migrate.init_app(app, db)
    csrf_protect.init_app(app)
    ma.init_app(app)
    user_manager = UserManager(
        app, db, User, UserInvitationClass=UserInvitation
    )

    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('scss/site.scss', filters='libsass', output='site.css')
    assets.register('scss_all', scss)

    # db.create_all(app=app)


def register_blueprints(app):
    """Register blueprints for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .cameras import cameras_blueprint
    app.register_blueprint(cameras_blueprint, url_prefix='/cameras')
    from .cards import cards_blueprint
    app.register_blueprint(cards_blueprint, url_prefix='/cards')
    from .species import species_blueprint
    app.register_blueprint(species_blueprint, url_prefix='/species')
    from .sites import sites_blueprint
    app.register_blueprint(sites_blueprint, url_prefix='/sites')
    from .surveys import surveys_blueprint
    app.register_blueprint(surveys_blueprint, url_prefix='/surveys')
    from .stats import stats_blueprint
    app.register_blueprint(stats_blueprint, url_prefix='/summary')
    from .reports import reports_blueprint
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
    from .validation import validation_blueprint
    app.register_blueprint(validation_blueprint, url_prefix='/validation')
