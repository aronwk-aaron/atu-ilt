from flask import (
    render_template,
    Blueprint,
    redirect,
    url_for
)
from app.models import (
    survey,
    site,
    card,
    camera,
    predator,
    survey_camera_card,
    survey_predator,
    survey_predator_camera,
)
from app.forms import (
    survey_form,
    survey_camera_form,
    survey_predator_form,
    survey_predator_camera_form
)

surveys_blueprint = Blueprint('surveys', __name__)


@surveys_blueprint.route('/')
def index():
    surveys = survey.query \
        .join(site, site.id == survey.site_id) \
        .add_columns(
            survey.id,
            survey.date,
            survey.ac1,
            survey.ac2,
            survey.ac3,
            site.name
        ).all()
    return render_template('surveys/index.jinja2', surveys=surveys)


@surveys_blueprint.route('/new', methods=('GET', 'POST'))
def new():
    form = survey_form()
    form.site.choices = [(s.id, s.name) for s in site.query.all()]
    if form.validate_on_submit():
        new_survey = survey(
            site_id=form.site.data,
            date=form.date.data,
            crew=form.crew.data,
            time_in=form.time_in.data,
            time_out=form.time_out.data,
            surveyed=form.precentage_surveyed.data,
            method=form.method.data,

            ac1=form.ac1.data,
            ac2=form.ac2.data,
            ac3=form.ac3.data,

            egg1=form.egg1.data,
            egg2=form.egg2.data,
            egg3=form.egg3.data,

            chick02=form.chick02.data,
            chick39=form.chick39.data,
            chick1017=form.chick1017.data,
            fledgling=form.fledgling.data,

            ef1=form.ef1.data,
            ef2=form.ef2.data,
            ef3=form.ef3.data,
            ef4=form.ef4.data,
            ef_com=form.ef_com.data,

            scrape=form.scrape.data,

            pveg=form.primary_vegitation.data,
            perc_pveg=form.precentage_primary_vegitation.data,

            cwdn1=form.cwdn1.data,
            cwdn2=form.cwdn2.data,
            cwdn3=form.cwdn3.data,
            cwdlog=form.cwdlog.data,

            w_temp=form.water_temp.data,
            a_temp=form.ambient_temp.data,
            perc_dio=form.precentage_disolved_oxygen.data,
            sal=form.salinity.data,
            sp_condu=form.specific_conductance.data,
            condu=form.conductivity.data,
        )
        new_survey.save()
        return redirect('/surveys')
    return render_template('surveys/new.jinja2', form=form)


@surveys_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    form = survey_form()
    form.site.choices = [(s.id, s.name) for s in site.query.all()]

    data = survey.query.filter(survey.id == id).first()

    if form.validate_on_submit():
        data.site_id = form.site.data
        data.date = form.date.data
        data.crew = form.crew.data
        data.time_in = form.time_in.data
        data.time_out = form.time_out.data
        data.surveyed = form.precentage_surveyed.data
        data.method = form.method.data

        data.ac1 = form.ac1.data
        data.ac2 = form.ac2.data
        data.ac3 = form.ac3.data

        data.egg1 = form.egg1.data
        data.egg2 = form.egg2.data
        data.egg3 = form.egg3.data
        data.scrape = form.scrape.data

        data.chick02 = form.chick02.data
        data.chick39 = form.chick39.data
        data.chick1017 = form.chick1017.data
        data.fledgling = form.fledgling.data

        data.ef1 = form.ef1.data
        data.ef2 = form.ef2.data
        data.ef3 = form.ef3.data
        data.ef4 = form.ef4.data
        data.ef_com = form.ef_com.data

        data.pveg = form.primary_vegitation.data
        data.perc_pveg = form.precentage_primary_vegitation.data

        data.cwdn1 = form.cwdn1.data
        data.cwdn2 = form.cwdn2.data
        data.cwdn3 = form.cwdn3.data
        data.cwdlog = form.cwdlog.data

        data.w_temp = form.water_temp.data
        data.a_temp = form.ambient_temp.data
        data.perc_dio = form.precentage_disolved_oxygen.data
        data.sal = form.salinity.data
        data.sp_condu = form.specific_conductance.data
        data.condu = form.conductivity.data
        data.save()
        return redirect(url_for('surveys.view', id=id))

    form.site.data = data.site_id
    form.date.data = data.date
    form.crew.data = data.crew
    form.time_in.data = data.time_in
    form.time_out.data = data.time_out
    form.precentage_surveyed.data = data.surveyed
    form.method.data = data.method

    form.ac1.data = data.ac1
    form.ac2.data = data.ac2
    form.ac3.data = data.ac3

    form.egg1.data = data.egg1
    form.egg2.data = data.egg2
    form.egg3.data = data.egg3

    form.chick02.data = data.chick02
    form.chick39.data = data.chick39
    form.chick1017.data = data.chick1017
    form.fledgling.data = data.fledgling

    form.ef1.data = data.ef1
    form.ef2.data = data.ef2
    form.ef3.data = data.ef3
    form.ef4.data = data.ef4
    form.ef_com.data = data.ef_com

    form.scrape.data = data.scrape

    form.primary_vegitation.data = data.pveg
    form.precentage_primary_vegitation.data = data.perc_pveg

    form.cwdn1.data = data.cwdn1
    form.cwdn2.data = data.cwdn2
    form.cwdn3.data = data.cwdn3
    form.cwdlog.data = data.cwdlog

    form.water_temp.data = data.w_temp
    form.ambient_temp.data = data.a_temp
    form.precentage_disolved_oxygen.data = data.perc_dio
    form.salinity.data = data.sal
    form.specific_conductance.data = data.sp_condu
    form.conductivity.data = data.condu

    return render_template('surveys/edit.jinja2', form=form)


@surveys_blueprint.route('/view/<id>')
def view(id):
    data = survey.query.filter(survey.id == id).first()

    cameras = survey_camera_card.query \
        .filter(data.id == survey_camera_card.survey_id).all()
    surveyed_predators = survey_predator.query \
        .filter(data.id == survey_predator.survey_id).all()
    recorded_predators = survey_predator_camera.query \
        .filter(data.id == survey_predator_camera.survey_id).all()

    return render_template(
        'surveys/view.jinja2',
        survey=data,
        cameras=cameras,
        surveyed_predators=surveyed_predators,
        recorded_predators=recorded_predators
    )


@surveys_blueprint.route('/<survey_id>/new_camera', methods=('GET', 'POST'))
def new_camera(survey_id):
    form = survey_camera_form()
    form.survey_id.data = survey_id
    form.camera.choices = [(c.id, c.name) for c in camera.query.all()]
    form.card_in.choices = [(ci.id, ci.name) for ci in card.query.all()]
    form.card_out.choices = [(co.id, co.name) for co in card.query.all()]

    if form.validate_on_submit():
        new_survey_camera = survey_camera_card(
            survey_id=form.survey_id.data,
            camera_id=form.camera.data,
            card_in_id=form.card_in.data,
            card_out_id=form.card_out.data,
            cleared=form.cleared.data,
            ch_bat=form.changed_battery.data,
            functional=form.functional.data,
            comment=form.comment.data
        )
        new_survey_camera.save()
        return redirect(url_for('surveys.view', id=survey_id))
    return render_template('surveys/camera/new.jinja2', form=form)


@surveys_blueprint.route(
    '/<survey_id>/edit_camera/<camera_id>',
    methods=('GET', 'POST')
)
def edit_camera(survey_id, camera_id):
    form = survey_camera_form()
    form.camera.choices = [(c.id, c.name) for c in camera.query.all()]
    form.card_in.choices = [(ci.id, ci.name) for ci in card.query.all()]
    form.card_out.choices = [(co.id, co.name) for co in card.query.all()]

    data = survey_camera_card.query \
        .filter(survey_id == survey_id, camera_id == camera_id).first()

    if form.validate_on_submit():
        data.survey_id = form.survey_id.data
        data.camera_id = form.camera.data
        data.card_in_id = form.card_in.data
        data.card_out_id = form.card_out.data
        data.cleared = form.cleared.data
        data.ch_bat = form.changed_battery.data
        data.functional = form.functional.data
        data.comment = form.comment.data
        data.save()
        return redirect(url_for('surveys.view', id=survey_id))

    form.survey_id.data = data.survey_id
    form.camera.data = data.camera_id
    form.card_in.data = data.card_in_id
    form.card_out.data = data.card_out_id
    form.cleared.data = data.cleared
    form.changed_battery.data = data.ch_bat
    form.functional.data = data.functional
    form.comment.data = data.comment

    return render_template('surveys/camera/new.jinja2', form=form)


@surveys_blueprint.route(
    '/<survey_id>/new_surveyed_predator',
    methods=('GET', 'POST')
)
def new_surveyed_predator(survey_id):
    form = survey_predator_form()
    form.survey_id.data = survey_id
    form.predator_id.choices = [
        (p.id, p.species) for p in predator.query.all()
    ]

    if form.validate_on_submit():
        new_survey_predator = survey_predator(
            survey_id=form.survey_id.data,
            sighting_type=form.sighting_type.data,
            predator_id=form.predator_id.data,
            count=form.count.data,
            comment=form.comment.data
        )
        new_survey_predator.save()
        return redirect(url_for('surveys.view', id=survey_id))
    return render_template('surveys/camera/new.jinja2', form=form)


@surveys_blueprint.route(
    '/<survey_id>/edit_surveyed_predator/<predator_id>/<sighting_type>',
    methods=('GET', 'POST')
)
def edit_surveyed_predator(survey_id, predator_id, sighting_type):
    form = survey_predator_form()
    form.predator_id.choices = [
        (p.id, p.species) for p in predator.query.all()
    ]

    data = survey_predator.query \
        .filter(
            survey_id == survey_id,
            predator_id == predator_id,
            sighting_type == sighting_type) \
        .first()

    if form.validate_on_submit():
        data.survey_id = form.survey_id.data
        data.sighting_type = form.sighting_type.data
        data.predator_id = form.predator_id.data
        data.count = form.count.data
        data.comment = form.comment.data
        data.save()
        return redirect(url_for('surveys.view', id=survey_id))

    form.survey_id.data = data.survey_id
    form.sighting_type.data = data.sighting_type
    form.predator_id.data = data.predator_id
    form.count.data = data.count
    form.comment.data = data.comment

    return render_template('surveys/camera/new.jinja2', form=form)


@surveys_blueprint.route(
    '/<survey_id>/new_recorded_predator',
    methods=('GET', 'POST')
)
def new_recorded_predator(survey_id):
    form = survey_predator_camera_form()
    form.survey_id.data = survey_id
    form.predator_id.choices = [
        (p.id, p.species) for p in predator.query.all()
    ]

    if form.validate_on_submit():
        new_survey_predator_camera = survey_predator_camera(
            survey_id=form.survey_id.data,
            predator_id=form.predator_id.data,
            start=form.start.data,
            end=form.end.data,
            count=form.count.data,
            scat=form.scat.data,
            adult_mort=form.adult_mort.data,
            chick_mort=form.chick_mort.data,
            nest_dest=form.nest_dest.data,
            comment=form.comment.data
        )
        new_survey_predator_camera.save()
        return redirect(url_for('surveys.view', id=survey_id))
    return render_template('surveys/camera/new.jinja2', form=form)


@surveys_blueprint.route(
    '/<survey_id>/edit_recorded_predator/<predator_id>/<start>/<end>',
    methods=('GET', 'POST')
)
def edit_recorded_predator(survey_id, predator_id, start, end):
    form = survey_predator_camera_form()
    form.predator_id.choices = [
        (p.id, p.species) for p in predator.query.all()
    ]

    data = survey_predator_camera.query \
        .filter(
            survey_id == survey_id,
            predator_id == predator_id,
            start == start,
            end == end) \
        .first()

    if form.validate_on_submit():
        data.survey_id = form.survey_id.data
        data.predator_id = form.predator_id.data
        data.start = form.start.data
        data.end = form.end.data
        data.count = form.count.data
        data.scat = form.scat.data
        data.adult_mort = form.adult_mort.data
        data.chick_mort = form.chick_mort.data
        data.nest_dest = form.nest_dest.data
        data.comment = form.comment.data
        data.save()
        return redirect(url_for('surveys.view', id=survey_id))

    form.survey_id.data = data.survey_id
    form.predator_id.data = data.predator_id
    form.start.data = data.start
    form.end.data = data.end
    form.count.data = data.count
    form.scat.data = data.scat
    form.adult_mort.data = data.adult_mort
    form.chick_mort.data = data.chick_mort
    form.nest_dest.data = data.nest_dest
    form.comment.data = data.comment

    return render_template('surveys/camera/new.jinja2', form=form)
