from flask import render_template, Blueprint, redirect
from app.models import site
from app.forms import site_form
from flask_user import roles_accepted, login_required

sites_blueprint = Blueprint('sites', __name__)


@sites_blueprint.route('/')
def index():
    sites = site.query.all()
    return render_template('sites/index.jinja2', sites=sites)


@sites_blueprint.route('/new', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def new():
    form = site_form()
    if form.validate_on_submit():
        new_site = site(
            name=form.name.data,
            loc_type=form.loc_type.data,
            elev=form.elevation.data,
            snag_perch=form.snag_perch.data,

            psub=form.primary_substrate.data,
            perc_psub=form.precentage_primary_substrate.data,
            silt_clay=form.silt_clay.data,
            sand=form.sand.data,
            gravel=form.gravel.data,
            sm_rocks=form.sm_rocks.data,
            perimeter=form.perimeter.data,

            est_area=form.est_area.data,
            perimeter_length=form.perimeter_length.data,
            mainland_distance=form.mainland_distance.data,
            length=form.length.data,
            comment=form.comment.data
        )
        new_site.save()
        return redirect('/sites')
    return render_template('sites/new.jinja2', form=form)


@sites_blueprint.route('/edit/<id>', methods=('GET', 'POST'))
@login_required
@roles_accepted('user', 'admin')
def edit(id):
    form = site_form()
    data = site.query.filter(site.id == id).first()

    if form.validate_on_submit():
        data.name = form.name.data
        data.loc_type = form.loc_type.data
        data.elev = form.elevation.data
        data.snag_perch = form.snag_perch.data

        data.psub = form.primary_substrate.data
        data.perc_psub = form.precentage_primary_substrate.data
        data.silt_clay = form.silt_clay.data
        data.sand = form.sand.data
        data.gravel = form.gravel.data
        data.sm_rocks = form.sm_rocks.data

        data.est_area = form.est_area.data
        data.perimeter_length = form.perimeter_length.data
        data.mainland_distance = form.mainland_distance.data
        data.length = form.length.data
        data.perimeter = form.perimeter.data
        data.comment = form.comment.data
        data.save()
        return redirect('/sites')

    form.name.data = data.name
    form.loc_type.data = data.loc_type

    form.elevation.data = data.elev
    form.snag_perch.data = data.snag_perch

    form.primary_substrate.data = data.psub
    form.precentage_primary_substrate.data = data.perc_psub
    form.silt_clay.data = data.silt_clay
    form.sand.data = data.sand
    form.gravel.data = data.gravel
    form.sm_rocks.data = data.sm_rocks

    form.perimeter.data = data.perimeter
    form.perimeter_length.data = data.perimeter_length
    form.mainland_distance.data = data.mainland_distance
    form.est_area.data = data.est_area
    form.length.data = data.length
    form.comment.data = data.comment

    return render_template('sites/edit.jinja2', form=form)


@sites_blueprint.route('/view/<id>')
def view(id):
    data = site.query.filter(site.id == id).all()
    return render_template('sites/view.jinja2', site=data)
