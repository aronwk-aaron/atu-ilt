from flask import render_template, Blueprint
from app.models import site, survey
from app.schemas import siteSchema, surveySchema
import json
import datetime
import copy

stats_blueprint = Blueprint('stats', __name__)

site_schema = siteSchema()
survey_schema = surveySchema()


@stats_blueprint.route('/')
def index():
    surveys = json.loads(
        survey_schema.jsonify(
            survey.query.order_by(survey.date).all(), many=True
        ).data
    )
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).all(), many=True
        ).data
    )
    site_data = gen_site_data(sites)
    survey_data = gen_survey_data(surveys)

    return render_template('stats/index.jinja2', data=site_data, survey_data=survey_data)


def gen_site_data(sites):
    data = {
        'sandbar_island': {
            'surveys': 0,
            'active': 0,
            'sites': 0,
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
            'sites': 0,
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
            'sites': 0,
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
    site_ef = []
    adult_div = 0
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
            data[sites[s]['loc_type'].replace(
                '-', '_')]['chick02'] += sites[s]['surveys'][i]['chick02']
            data[sites[s]['loc_type'].replace(
                '-', '_')]['chick39'] += sites[s]['surveys'][i]['chick39']
            data[sites[s]['loc_type'].replace(
                '-', '_')]['chick1017'] += sites[s]['surveys'][i]['chick1017']
            data[sites[s]['loc_type'].replace(
                '-', '_')]['egg'] += sites[s]['surveys'][i]['egg1']
            data[sites[s]['loc_type'].replace(
                '-', '_')]['egg'] += sites[s]['surveys'][i]['egg2'] * 2
            data[sites[s]['loc_type'].replace(
                '-', '_')]['egg'] += sites[s]['surveys'][i]['egg3'] * 3
            data[sites[s]['loc_type'].replace(
                '-', '_')]['fledge'] += sites[s]['surveys'][i]['fledgling']
            # getting avg site data
            if sites[s]['surveys'][i]['ac1'] > 0:
                adult_div += 1
            if sites[s]['surveys'][i]['ac2'] > 0:
                adult_div += 1
            if sites[s]['surveys'][i]['ac3'] > 0:
                adult_div += 1
            if adult_div > 0:
                site_avgs.append(
                    (
                        sites[s]['surveys'][i]['ac1'] +
                        sites[s]['surveys'][i]['ac2'] +
                        sites[s]['surveys'][i]['ac3']
                    )/adult_div
                )
            else:
                site_avgs.append(0)
            adult_div = 0
            site_ef.append(sites[s]['surveys'][i]['ef1'])
            site_ef.append(sites[s]['surveys'][i]['ef2'])
            site_ef.append(sites[s]['surveys'][i]['ef3'])
            site_ef.append(sites[s]['surveys'][i]['ef4'])
            # counts for specific site to aid in other data
            site_count['adult_count'] += (
                sites[s]['surveys'][i]['ac1'] +
                sites[s]['surveys'][i]['ac2'] +
                sites[s]['surveys'][i]['ac3']
            )/3
            site_count['chick02'] += sites[s]['surveys'][i]['chick02']
            site_count['chick39'] += sites[s]['surveys'][i]['chick39']
            site_count['chick1017'] += sites[s]['surveys'][i]['chick1017']
            site_count['egg'] += sites[s]['surveys'][i]['egg1']
            site_count['egg'] += sites[s]['surveys'][i]['egg2'] * 2
            site_count['egg'] += sites[s]['surveys'][i]['egg3'] * 3
            site_count['fledge'] += sites[s]['surveys'][i]['fledgling']
        # end iterating over surveys for site
        data[sites[s]['loc_type'].replace(
            '-', '_')]['adult_count'] += max(site_avgs)
        data[sites[s]['loc_type'].replace('-', '_')]['sites'] += 1
        if ((site_count['adult_count'] > 0) and (
            (site_count['egg'] > 0) or
            (site_count['chick02'] > 0) or
            (site_count['chick39'] > 0) or
            (site_count['chick1017'] > 0) or
            (site_count['fledge'] > 0)
        )):
            data[sites[s]['loc_type'].replace('-', '_')]['active'] += 1
        if len(site_ef) > 0:
            for egg in range(len(site_ef)):
                if site_ef[egg] == 'NA':
                    continue
                if site_ef[egg] == 'i+':
                    site_ef[egg] = ord('j')
                    continue
                site_ef[egg] = ord(site_ef[egg])
            highest_ef = site_ef[0]
            for egg in range(len(site_ef)):
                if str(site_ef[egg]) == 'NA':
                    if highest_ef == 'NA' and ((egg + 1) != len(site_ef)):
                        highest_ef = site_ef[egg + 1]
                    continue
                if highest_ef <= site_ef[egg]:
                    highest_ef = site_ef[egg]
                else:  # variance of eggs in a site!!!!!
                    if (highest_ef - site_ef[egg]) > 4:
                        data[sites[s]['loc_type'].replace(
                            '-', '_')]['nestingattempts'] += 1
                        highest_ef = site_ef[egg]
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
        site_ef.clear()

    return data


def gen_survey_data(surveys):
    data = [['Day', ' Adults', 'Fledgelings', 'Chicks', 'Eggs']]

    start_season_date = datetime.date(2020, 6, 15)
    end_season_date = datetime.date(2020, 8, 31)
    current_season_date = datetime.date(2020, 6, 15)
    two_weeks = datetime.timedelta(days=14)
    one_day = datetime.timedelta(days=1)
    while current_season_date < end_season_date:
        end_itter_date = current_season_date + two_weeks
        itter_data = [current_season_date, 0, 0, 0, 0]
        for surv in surveys:
            surv_date = datetime.date.fromisoformat(surv["date"])
            if surv_date < start_season_date or surv_date > end_season_date:
                continue  # not part of the season
            elif current_season_date <= surv_date < end_itter_date:
                adult_div = 0
                if surv["ac1"] > 0:
                    adult_div += 1
                if surv["ac2"] > 0:
                    adult_div += 1
                if surv["ac3"] > 0:
                    adult_div += 1
                if adult_div > 0:
                    itter_data[1] = itter_data[1] + (
                            surv["ac1"] +
                            surv["ac2"] +
                            surv["ac3"]
                        )/adult_div
                itter_data[2] = itter_data[2] + surv["fledgling"]
                itter_data[3] = itter_data[3] + (surv["chick02"] + surv["chick39"] + surv["chick1017"])
                itter_data[4] = itter_data[4] + (surv["egg1"] + (surv["egg2"] * 2) + (surv["egg3"] * 3))
        data.append(itter_data)
        current_season_date += one_day
    return data
