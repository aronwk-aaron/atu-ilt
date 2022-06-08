from flask import render_template, Blueprint, redirect, send_file
from app.forms import image_form
from flask_user import roles_accepted, login_required
from werkzeug.utils import secure_filename
import pathlib

images_blueprint = Blueprint('images', __name__)


@images_blueprint.route('/')
def index():
    images = pathlib.Path('app/static/uploads')
    images.resolve().mkdir(parents=True, exist_ok=True)
    files = [path for path in images.rglob(".*") if path.is_file()]
    return render_template('images/index.jinja2', images=len(files))


@images_blueprint.route('/upload', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def upload():

    form = image_form()
    if form.validate_on_submit():
        print(form.file.data)
        f = form.file.data
        name = secure_filename(f.filename)
        f.save("app/static/uploads/" + name)
        return redirect('/images')
    return render_template('images/new.jinja2', form=form)


@images_blueprint.route('/get/<id>')
def get(id):
    images = pathlib.Path('app/static/uploads')
    files = [path for path in images.rglob("*") if path.is_file()]
    return send_file(files[int(id)].resolve())

# @images_blueprint.route('/delete/', methods=('GET', 'POST'))
# @login_required
# @roles_accepted('user', 'admin')
# def delete(id):
#     form = image_form()
#     data = image.query.filter(image.id == id).first()

#     if form.validate_on_submit():
#         data.name = form.name.data,
#         data.size = form.size.data
#         data.save()
#         return redirect('/images')
#     form.name.data = data.name
#     form.size.data = data.size
#     return render_template('images/edit.jinja2', form=form)
