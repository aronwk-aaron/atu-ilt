from flask import render_template, Blueprint, redirect
from app.models import camera
from app.forms import camera_form

cameras_blueprint = Blueprint('cameras', __name__)


@cameras_blueprint.route('/')
def index():
    cameras = camera.query.all()
    return render_template('cameras/index.jinja2', cameras=cameras)


@cameras_blueprint.route('/new', methods=('GET', 'POST'))
def new():
    form = camera_form()
    if form.validate_on_submit():
        new_camera = camera(
            name=form.name.data,
            brand=form.brand.data,
            functional=form.functional.data,
            comment=form.comment.data
        )
        new_camera.save()
        return redirect('/cameras')
    return render_template('cameras/new.jinja2', form=form)


@cameras_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    form = camera_form()
    data = camera.query.filter(camera.id == id).first()

    if form.validate_on_submit():
        data.name = form.name.data
        data.brand = form.brand.data
        data.functional = form.functional.data
        data.comment = form.comment.data
        data.save()
        return redirect('/cameras')
    form.name.data = data.name
    form.brand.data = data.brand
    form.functional.data = data.functional
    form.comment.data = data.comment
    return render_template('cameras/edit.jinja2', form=form)
