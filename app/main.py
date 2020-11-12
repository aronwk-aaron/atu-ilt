from flask import render_template, Blueprint
from flask_user import login_required, roles_required
from app.models import User

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    """Home/Index Page"""
    return render_template('main/index.jinja2')


@main_blueprint.route('/about')
def about():
    """About Page"""
    return render_template('main/about.jinja2')


@main_blueprint.route('/users', methods=['GET'])
@login_required
@roles_required('admin')
def users():
    user_list = User.get_all()
    return render_template('main/users.jinja2', users=user_list)
