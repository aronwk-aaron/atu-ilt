from flask import render_template, Blueprint, redirect
from app.models import predator
from app.forms import predator_form
from flask_user import roles_accepted, login_required

predators_blueprint = Blueprint('predators', __name__)


@predators_blueprint.route('/')
def index():
    predators = predator.query.all()
    return render_template('predators/index.jinja2', predators=predators)


@predators_blueprint.route('/new', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def new():
    form = predator_form()
    if form.validate_on_submit():
        new_predator = predator(
            species=form.species.data,
            predator_type=form.predator_type.data,
            classification=form.classification.data,
            risk=form.risk.data
        )
        new_predator.save()
        return redirect('/predators')
    return render_template('predators/new.jinja2', form=form)


@predators_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def edit(id):
    form = predator_form()
    data = predator.query.filter(predator.id == id).first()

    if form.validate_on_submit():
        data.species = form.species.data,
        data.predator_type = form.predator_type.data
        data.classification = form.classification.data
        data.risk = form.risk.data
        data.save()
        return redirect('/predators')
    form.species.data = data.species
    form.predator_type.data = data.predator_type
    form.risk.data = data.risk
    form.classification.data = data.classification
    return render_template('predators/edit.jinja2', form=form)
