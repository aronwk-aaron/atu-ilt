from flask import render_template, Blueprint, redirect
from app.models import card
from app.forms import card_form

cards_blueprint = Blueprint('cards', __name__)


@cards_blueprint.route('/')
def index():
    cards = card.query.all()
    return render_template('cards/index.jinja2', cards=cards)


@cards_blueprint.route('/new', methods=('GET', 'POST'))
def new():
    form = card_form()
    if form.validate_on_submit():
        new_card = card(
            name=form.name.data,
            size=form.size.data
        )
        new_card.save()
        return redirect('/cards')
    return render_template('cards/new.jinja2', form=form)


@cards_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    form = card_form()
    data = card.query.filter(card.id == id).first()

    if form.validate_on_submit():
        data.name = form.name.data,
        data.size = form.size.data
        data.save()
        return redirect('/cards')
    form.name.data = data.name
    form.size.data = data.size
    return render_template('cards/edit.jinja2', form=form)
