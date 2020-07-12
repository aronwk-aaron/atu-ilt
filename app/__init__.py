from flask import Flask
from flask_assets import Environment
from webassets import Bundle

from app.models import db, migrate
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect

# from app.models import User, Role, UsersRoles
from app.commands import init_db


# Instantiate Flask extensions
ma = Marshmallow()
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
    app.config.from_object('app.local_settings')

    register_extensions(app)
    register_blueprints(app)
    # add the init_db command to flask cli
    app.cli.add_command(init_db)

    return app


def register_extensions(app):
    """Register extensions for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    csrf_protect.init_app(app)


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

    # from .submissions import submissions_blueprint
    # app.register_blueprint(submissions_blueprint, url_prefix='/submissions')
    # from .revisions import revisions_blueprint
    # app.register_blueprint(revisions_blueprint, url_prefix='/revisions')
