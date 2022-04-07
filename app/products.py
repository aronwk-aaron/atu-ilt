from flask import render_template, Blueprint

products_blueprint = Blueprint('products', __name__)


@products_blueprint.route('/atu_gs_2021')
def atu_gs_2021():
    return render_template('products/atugs2021.html.j2')


@products_blueprint.route('/atu_gs_2022')
def atu_gs_2022():
    return render_template('products/atugs2022.html.j2')
