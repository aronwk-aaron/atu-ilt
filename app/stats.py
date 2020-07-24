from flask import render_template, Blueprint
from app.models import survey

stats_blueprint = Blueprint('stats', __name__)


@stats_blueprint.route('/')
def index():
    surveys = survey.query.order_by(survey.site_id).order_by(survey.date).all()
    return render_template('stats/index.jinja2', surveys=surveys)
