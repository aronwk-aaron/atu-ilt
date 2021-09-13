from flask import render_template, Blueprint, redirect
from app.models import camera, survey, survey_camera_card
from app.forms import camera_form
from flask_user import roles_accepted, login_required
from app.schemas import surveySchema, cameraSchema
import json
import datetime

cameras_blueprint = Blueprint('cameras', __name__)

survey_schema = surveySchema()
camera_schema = cameraSchema()


@cameras_blueprint.route('/')
def index():

    surveys = json.loads(
        survey_schema.jsonify(
            survey.query.all(), many=True
        ).data
    )

    cameras = json.loads(
        camera_schema.jsonify(
            camera.query.all(), many=True
        ).data
    )

    start_2020 = datetime.date(2020, 1, 1)
    end_2020 = datetime.date(2020, 12, 31)

    start_2021 = datetime.date(2021, 1, 1)
    end_2021 = datetime.date(2021, 12, 31)

    for c in range(len(cameras)):
        cameras[c]["used"] = []
        for s in range(len(surveys)):
            date = datetime.date.fromisoformat(surveys[s]["date"])
            for used_camera in range(len(surveys[s]["cameras"])):
                if date > start_2020 and date < end_2020 and \
                   "2020" not in cameras[c]["used"] and \
                   cameras[c]["id"] == surveys[s]["cameras"][used_camera]["camera_id"]:
                    cameras[c]["used"].append("2020")
                if date > start_2021 and date < end_2021 and \
                   "2021" not in cameras[c]["used"] and \
                   cameras[c]["id"] == surveys[s]["cameras"][used_camera]["camera_id"]:
                    cameras[c]["used"].append("2021")

    return render_template('cameras/index.jinja2', cameras=cameras)


@cameras_blueprint.route('/new', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
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
@login_required
@roles_accepted('user', 'admin')
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


@cameras_blueprint.route('/view/<id>')
def view(id):
    camera_data = camera.query.filter(camera.id == id).first()
    surveys = survey.query.join(survey_camera_card).filter(survey_camera_card.camera_id == id).all()
    return render_template(
        'cameras/view.jinja2',
        surveys=surveys,
        camera=camera_data
    )
