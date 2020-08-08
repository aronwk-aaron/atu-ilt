from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    """Home/Index Page"""
    return render_template('main/index.jinja2')


@main_blueprint.route('/about')
def about():
    """about Page"""
    return render_template('main/about.jinja2')
