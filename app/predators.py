from flask import render_template, Blueprint, redirect
from app.models import predator
from app.forms import predator_form

predators_blueprint = Blueprint('predators', __name__)


@predators_blueprint.route('/')
def index():
    predators = predator.query.all()
    return render_template('predators/index.jinja2', predators=predators)


@predators_blueprint.route('/new', methods=('GET', 'POST'))
def new():
    form = predator_form()
    if form.validate_on_submit():
        new_predator = predator(
            species=form.species.data,
            predator_type=form.predator_type.data,
            volatility=form.volatility.data
        )
        new_predator.save()
        return redirect('/predators')
    return render_template('predators/new.jinja2', form=form)


@predators_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    form = predator_form()
    data = predator.query.filter(predator.id == id).first()

    if form.validate_on_submit():
        data.species = form.species.data,
        data.predator_type = form.predator_type.data
        data.volatility = form.volatility.data
        data.save()
        return redirect('/predators')
    form.species.data = data.species
    form.predator_type.data = data.predator_type
    form.volatility.data = data.volatility
    return render_template('predators/edit.jinja2', form=form)
