from flask import render_template, Blueprint, redirect
from app.models import site
from app.forms import site_form

sites_blueprint = Blueprint('sites', __name__)


@sites_blueprint.route('/')
def index():
    sites = site.query.all()
    return render_template('sites/index.jinja2', sites=sites)


@sites_blueprint.route('/new', methods=('GET', 'POST'))
def new():
    form = site_form()
    if form.validate_on_submit():
        new_site = site(
            name=form.name.data,
            loc_type=form.loc_type.data,
            size_type=form.size_type.data,
            est_area=form.est_area.data,
            length=form.length.data
        )
        new_site.save()
        return redirect('/sites')
    return render_template('sites/new.jinja2', form=form)


@sites_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    form = site_form()
    data = site.query.filter(site.id == id).first()

    if form.validate_on_submit():
        data.name = form.name.data,
        data.loc_type = form.loc_type.data,
        data.size_type = form.size_type.data,
        data.est_area = form.est_area.data,
        data.length = form.length.data
        data.data.save()
        return redirect('/sites')

    form.name.data = data.name
    form.loc_type.data = data.loc_type
    form.size_type.data = data.size_type
    form.est_area.data = data.est_area
    form.length.data = data.length

    return render_template('sites/edit.jinja2', form=form)
