import os
import datetime
from flask import Flask
from flask_assets import Environment
from webassets import Bundle

from app.models import db, migrate
from app.schemas import ma
from flask_wtf.csrf import CSRFProtect

from app.commands import init_db


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

    def calc_datetime(value, stop):
        difference = stop - value
        return difference

    app.jinja_env.filters['time_delta'] = calc_datetime

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
    csrf_protect.init_app(app)
    ma.init_app(app)

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
    from .predators import predators_blueprint
    app.register_blueprint(predators_blueprint, url_prefix='/predators')
    from .sites import sites_blueprint
    app.register_blueprint(sites_blueprint, url_prefix='/sites')
    from .surveys import surveys_blueprint
    app.register_blueprint(surveys_blueprint, url_prefix='/surveys')
    from .stats import stats_blueprint
    app.register_blueprint(stats_blueprint, url_prefix='/stats')
    from .reports import reports_blueprint
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
