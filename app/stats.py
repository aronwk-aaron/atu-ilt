from flask import render_template, Blueprint
from app.models import site
from app.schemas import siteSchema
import json

stats_blueprint = Blueprint('stats', __name__)

site_schema = siteSchema()


@stats_blueprint.route('/')
def index():
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).all(), many=True
        ).data
    )
    data = {
        'surveys': 0,
        'adult_count': 0,
        'egg': 0,
        'chick02': 0,
        'chick39': 0,
        'chick1017': 0,
        'fledge': 0,
        'renest': 0
    }
    site_avgs = []
    for s in sites:
        for i in range(len(s['surveys'])):
            data['surveys'] += 1
            data['chick02'] += s['surveys'][i]['chick02']
            data['chick39'] += s['surveys'][i]['chick39']
            data['chick1017'] += s['surveys'][i]['chick1017']
            data['egg'] += s['surveys'][i]['egg1']
            data['egg'] += s['surveys'][i]['egg2'] * 2
            data['egg'] += s['surveys'][i]['egg3'] * 3
            data['fledge'] += s['surveys'][i]['fledgling']
            # print(site_avgs)
            if i == 0:
                site_avgs.append(
                    (
                        s['surveys'][i]['ac1'] +
                        s['surveys'][i]['ac2'] +
                        s['surveys'][i]['ac3']
                    )/3
                )
            elif s['surveys'][i]['site_id'] == s['surveys'][i - 1]['site_id']:
                # print(f'adding: {max(site_avgs)}')
                data['adult_count'] += max(site_avgs)
                site_avgs = []
                site_avgs.append(
                    (
                        s['surveys'][i]['ac1'] +
                        s['surveys'][i]['ac2'] +
                        s['surveys'][i]['ac3']
                    )/3
                )
            else:
                site_avgs.append(
                    (
                        s['surveys'][i]['ac1'] +
                        s['surveys'][i]['ac2'] +
                        s['surveys'][i]['ac3']
                    )/3
                )

    return render_template('stats/index.jinja2', data=data)
