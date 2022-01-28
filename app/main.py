from flask import send_from_directory, render_template, Blueprint, redirect, url_for
from flask_user import login_required, roles_required
from app.models import User, UserInvitation, UsersRoles

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
    invitations = UserInvitation.query.all()
    return render_template(
        'main/users.jinja2',
        users=user_list,
        invites=invitations
    )


@main_blueprint.route('/users/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def delete_user(id):
    if id != 1:
        User.get_user_by_id(user_id=id).delete()
    return redirect(url_for('main.users'))


@main_blueprint.route('/users/delete_invite/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def delete_invite(id):
    UserInvitation.query.filter(UserInvitation.id == id).first().delete()
    return redirect(url_for('main.users'))


@main_blueprint.route('/users/edit_role/<user_id>/<role_id>', methods=['GET'])
@login_required
@roles_required('admin')
def edit_role(user_id, role_id):
    if user_id != 1:
        UsersRoles.update_userrole(user_id=user_id, role_id=role_id)
    return redirect(url_for('main.users'))


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static/logo/',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
