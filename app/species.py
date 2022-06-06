from flask import render_template, Blueprint, redirect
from app.models import species, survey_species, survey_species_camera
from app.forms import species_form
from flask_user import roles_accepted, login_required

species_blueprint = Blueprint('species', __name__)


@species_blueprint.route('/')
def index():
    species_query = species.query.all()
    return render_template('species/index.jinja2', species=species_query)


@species_blueprint.route('/view/<id>')
def view(id):
    recorded_species = survey_species_camera.query.filter(
        survey_species_camera.species_id == id).all()
    surveyed_species = survey_species.query.filter(
        survey_species.species_id == id).all()
    speci = species.query.filter(species.id == id).first()
    return render_template(
        'species/view.jinja2',
        speci=speci,
        recorded_species=recorded_species,
        surveyed_species=surveyed_species
    )


@species_blueprint.route('/new', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def new():
    form = species_form()
    if form.validate_on_submit():
        new_species = species(
            species=form.species.data,
            species_type=form.species_type.data,
            classification=form.classification.data,
            risk=form.risk.data,
            group=form.group.data
        )
        new_species.save()
        return redirect('/species')
    return render_template('species/new.jinja2', form=form)


@species_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def edit(id):
    form = species_form()
    data = species.query.filter(species.id == id).first()

    if form.validate_on_submit():
        data.species = form.species.data,
        data.species_type = form.species_type.data
        data.classification = form.classification.data
        data.risk = form.risk.data
        data.group = form.group.data
        data.save()
        return redirect('/species')
    form.species.data = data.species
    form.species_type.data = data.species_type
    form.risk.data = data.risk
    form.group.data = data.group
    form.classification.data = data.classification
    return render_template('species/edit.jinja2', form=form)
