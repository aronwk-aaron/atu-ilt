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
        'sandbar_island': {
            'surveys': 0,
            'active': 0,
            'adult_count': 0,
            'egg': 0,
            'chick02': 0,
            'chick39': 0,
            'chick1017': 0,
            'fledge': 0,
            'nestingattempts': 0
        },
        'sandbar_main': {
            'surveys': 0,
            'active': 0,
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
            'active': 0,
            'adult_count': 0,
            'egg': 0,
            'chick02': 0,
            'chick39': 0,
            'chick1017': 0,
            'fledge': 0,
            'nestingattempts': 0
        }
    }
    site_avgs = [0]
    site_count = {
        'adult_count': 0,
        'egg': 0,
        'chick02': 0,
        'chick39': 0,
        'chick1017': 0,
        'fledge': 0,
    }
    for s in range(len(sites)):  # for each site
        for i in range(len(sites[s]['surveys'])):  # for each survey in a site
            # simple counts per site type
            data[sites[s]['loc_type'].replace('-', '_')]['surveys'] += 1
            data[sites[s]['loc_type'].replace('-', '_')]['chick02'] += sites[s]['surveys'][i]['chick02']
            data[sites[s]['loc_type'].replace('-', '_')]['chick39'] += sites[s]['surveys'][i]['chick39']
            data[sites[s]['loc_type'].replace('-', '_')]['chick1017'] += sites[s]['surveys'][i]['chick1017']
            data[sites[s]['loc_type'].replace('-', '_')]['egg'] += sites[s]['surveys'][i]['egg1']
            data[sites[s]['loc_type'].replace('-', '_')]['egg'] += sites[s]['surveys'][i]['egg2'] * 2
            data[sites[s]['loc_type'].replace('-', '_')]['egg'] += sites[s]['surveys'][i]['egg3'] * 3
            data[sites[s]['loc_type'].replace('-', '_')]['fledge'] += sites[s]['surveys'][i]['fledgling']
            # getting avg site data
            site_avgs.append(
                (
                    sites[s]['surveys'][i]['ac1'] +
                    sites[s]['surveys'][i]['ac2'] +
                    sites[s]['surveys'][i]['ac3']
                )/3
            )
            # counts for specific site to aid in other data
            site_count['adult_count'] += (
                sites[s]['surveys'][i]['ac1'] +
                sites[s]['surveys'][i]['ac2'] +
                sites[s]['surveys'][i]['ac3']
            )
            site_count['chick02'] += sites[s]['surveys'][i]['chick02']
            site_count['chick39'] += sites[s]['surveys'][i]['chick39']
            site_count['chick1017'] += sites[s]['surveys'][i]['chick1017']
            site_count['egg'] += sites[s]['surveys'][i]['egg1']
            site_count['egg'] += sites[s]['surveys'][i]['egg2'] * 2
            site_count['egg'] += sites[s]['surveys'][i]['egg3'] * 3
            site_count['fledge'] += sites[s]['surveys'][i]['fledgling']
        # end iterating over surveys for site
        data[sites[s]['loc_type'].replace('-', '_')]['adult_count'] += max(site_avgs)
        if ((site_count['adult_count'] > 0) and (
            (site_count['egg'] > 0) or
            (site_count['chick02'] > 0) or
            (site_count['chick39'] > 0) or
            (site_count['chick1017'] > 0) or
            (site_count['fledge'] > 0)
        )):
            data[sites[s]['loc_type'].replace('-', '_')]['active'] += 1

        # reset for next site
        site_count = {
            'adult_count': 0,
            'egg': 0,
            'chick02': 0,
            'chick39': 0,
            'chick1017': 0,
            'fledge': 0,
        }
        site_avgs = [0]

    return render_template('stats/index.jinja2', data=data)
