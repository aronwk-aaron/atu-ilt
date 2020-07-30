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
        'river': {
            'surveys': 0,
            'adult_count': 0,
            'egg': 0,
            'chick02': 0,
            'chick39': 0,
            'chick1017': 0,
            'fledge': 0,
            'nestingattempts': 0
        },
        'rooftop': {
            'surveys': 0,
            'adult_count': 0,
            'egg': 0,
            'chick02': 0,
            'chick39': 0,
            'chick1017': 0,
            'fledge': 0,
            'nestingattempts': 0
        }
    }
    site_avgs = []
    for s in range(len(sites)):
        for i in range(len(sites[s]['surveys'])):
            if sites[s]['loc_type'] == 'rooftop':
                data['rooftop']['surveys'] += 1
                data['rooftop']['chick02'] += sites[s]['surveys'][i]['chick02']
                data['rooftop']['chick39'] += sites[s]['surveys'][i]['chick39']
                data['rooftop']['chick1017'] += sites[s]['surveys'][i]['chick1017']
                data['rooftop']['egg'] += sites[s]['surveys'][i]['egg1']
                data['rooftop']['egg'] += sites[s]['surveys'][i]['egg2'] * 2
                data['rooftop']['egg'] += sites[s]['surveys'][i]['egg3'] * 3
                data['rooftop']['fledge'] += sites[s]['surveys'][i]['fledgling']
            else:
                data['river']['surveys'] += 1
                data['river']['chick02'] += sites[s]['surveys'][i]['chick02']
                data['river']['chick39'] += sites[s]['surveys'][i]['chick39']
                data['river']['chick1017'] += sites[s]['surveys'][i]['chick1017']
                data['river']['egg'] += sites[s]['surveys'][i]['egg1']
                data['river']['egg'] += sites[s]['surveys'][i]['egg2'] * 2
                data['river']['egg'] += sites[s]['surveys'][i]['egg3'] * 3
                data['river']['fledge'] += sites[s]['surveys'][i]['fledgling']
            if i == 0:
                site_avgs.append(
                    (
                        sites[s]['surveys'][i]['ac1'] +
                        sites[s]['surveys'][i]['ac2'] +
                        sites[s]['surveys'][i]['ac3']
                    )/3
                )
            elif sites[s]['surveys'][i]['site_id'] == sites[s]['surveys'][i - 1]['site_id']:
                if sites[s - 1]['loc_type'] == 'rooftop':
                    data['rooftop']['adult_count'] += max(site_avgs)
                else:
                    data['river']['adult_count'] += max(site_avgs)
                site_avgs = []
                site_avgs.append(
                    (
                        sites[s]['surveys'][i]['ac1'] +
                        sites[s]['surveys'][i]['ac2'] +
                        sites[s]['surveys'][i]['ac3']
                    )/3
                )
            else:
                print('else')
                site_avgs.append(
                    (
                        sites[s]['surveys'][i]['ac1'] +
                        sites[s]['surveys'][i]['ac2'] +
                        sites[s]['surveys'][i]['ac3']
                    )/3
                )

    return render_template('stats/index.jinja2', data=data)
