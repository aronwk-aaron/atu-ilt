from flask import render_template, Blueprint
from app.models import (
    site
)
from app.schemas import (
    siteSchema
)
import json
import datetime
import re

reports_blueprint = Blueprint('reports', __name__)

site_schema = siteSchema()


@reports_blueprint.route('/')
def index():
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).all(), many=True
        ).data
    )

    # Season time setup
    start_2020_season_date = datetime.date(2020, 1, 1)
    end_2020_season_date = datetime.date(2020, 12, 31)

    start_2021_season_date = datetime.date(2021, 1, 1)
    end_2021_season_date = datetime.date(2021, 12, 31)

    # This is actually the peak of the season dates based on 2 week stats
    start_2020_peak_date = datetime.date(2020, 7, 4)
    end_2020_peak_date = datetime.date(2020, 7, 18)

    start_2021_peak_date = datetime.date(2021, 5, 1)
    end_2021_peak_date = datetime.date(2021, 9, 30)

    # Site Name | Nests | Chicks | Fledglings | Adults
    header = [
        'Colony Location',
        'Nests',
        'Chicks',
        'Fledglings',
        'Adult Avg.',
        'Initiation Date'
    ]

    data_2020 = []
    data_2021 = []

    for s in range(len(sites)):
        tmp_2020 = ['ERROR', 0, 0, 0, 0, None, 0]
        tmp_2021 = ['ERROR', 0, 0, 0, 0, None, 0]
        for x in (
            (
                [
                    item['date'],
                    item['egg1'] + item['egg2'] + item['egg3'],
                    item['chick02'] + item['chick39'] + item['chick1017'],
                    item['fledgling'],
                    adult_avg(item['ac1'], item['ac2'], item['ac3']),
                    [
                        ef_str_to_num(item['ef1']),
                        ef_str_to_num(item['ef2']),
                        ef_str_to_num(item['ef3']),
                        ef_str_to_num(item['ef4'])
                    ]
                ]
            )
                for item in sites[s]['surveys']):
            surv_date = datetime.date.fromisoformat(
                x[0]
            )

            # if 2020
            if surv_date > start_2020_season_date and \
                    surv_date < end_2020_season_date:
                tmp_2020[0] = sites[s]['name']
                if (x[1] + x[2] + x[3] + x[4] > 0) and not tmp_2020[6]:
                    tmp_2020[6] = surv_date
                if not tmp_2020[5] and any(egg > 0 for egg in x[5]):
                    tmp_2020[5] = surv_date - datetime.timedelta(
                            days=max(x[5])
                        )
            if surv_date > start_2020_peak_date and \
                    surv_date < end_2020_peak_date:
                if tmp_2020[4] < x[4]:
                    # want new one
                    tmp_2020[1] = x[1]
                    tmp_2020[2] = x[2]
                    tmp_2020[3] = x[3]
                    tmp_2020[4] = x[4]
                elif tmp_2020[4] == [4]:
                    if tmp_2020[3] < x[3]:
                        # want new one
                        tmp_2020[1] = x[1]
                        tmp_2020[2] = x[2]
                        tmp_2020[3] = x[3]
                        tmp_2020[4] = x[4]
                    elif tmp_2020[3] == [3]:
                        if tmp_2020[2] < x[2]:
                            # want new one
                            tmp_2020[1] = x[1]
                            tmp_2020[2] = x[2]
                            tmp_2020[3] = x[3]
                            tmp_2020[4] = x[4]
                        elif tmp_2020[2] == [2]:
                            if tmp_2020[1] < x[1]:
                                # want new one
                                tmp_2020[1] = x[1]
                                tmp_2020[2] = x[2]
                                tmp_2020[3] = x[3]
                                tmp_2020[4] = x[4]
                            elif tmp_2020[1] == [1]:
                                # want new one
                                tmp_2020[1] = x[1]
                                tmp_2020[2] = x[2]
                                tmp_2020[3] = x[3]
                                tmp_2020[4] = x[4]

            # else if 2021
            if surv_date > start_2021_season_date and \
                    surv_date < end_2021_season_date:
                tmp_2021[0] = sites[s]['name']
                if (x[1] + x[2] + x[3] + x[4] > 0) and not tmp_2021[6]:
                    tmp_2021[6] = surv_date
                if not tmp_2021[5] and any(egg > 0 for egg in x[5]):
                    tmp_2021[5] = surv_date - datetime.timedelta(
                            days=max(x[5])
                        )
            elif surv_date > start_2021_peak_date and \
                    surv_date < end_2021_peak_date:
                if tmp_2021[4] < x[4]:
                    # want new one
                    tmp_2021[1] = x[1]
                    tmp_2021[2] = x[2]
                    tmp_2021[3] = x[3]
                    tmp_2021[4] = x[4]
                elif tmp_2021[4] == [4]:
                    if tmp_2021[3] < x[3]:
                        # want new one
                        tmp_2021[1] = x[1]
                        tmp_2021[2] = x[2]
                        tmp_2021[3] = x[3]
                        tmp_2021[4] = x[4]
                    elif tmp_2021[3] == [3]:
                        if tmp_2021[2] < x[2]:
                            # want new one
                            tmp_2021[1] = x[1]
                            tmp_2021[2] = x[2]
                            tmp_2021[3] = x[3]
                        elif tmp_20212 == 2:
                            if tmp_2021[1] < x[1]:
                                # want new one
                                tmp_2021[1] = x[1]
                                tmp_2021[2] = x[2]
                                tmp_2021[3] = x[3]
                                tmp_2021[4] = x[4]
                            elif tmp_2021[1] == [1]:
                                # want new one
                                tmp_2021[1] = x[1]
                                tmp_2021[2] = x[2]
                                tmp_2021[3] = x[3]
                                tmp_2021[4] = x[4]


        if (tmp_2020[0] != 'ERROR') and ((tmp_2020[1] + tmp_2020[2] + tmp_2020[3] + tmp_2020[4]) > 0):
            data_2020.append(tmp_2020)
        if (tmp_2021[0] != 'ERROR') and ((tmp_2021[1] + tmp_2021[2] + tmp_2021[3] + tmp_2021[4]) > 0):
            data_2021.append(tmp_2021)

    # Sort by site name (index 0)

    data_2020.sort(key=lambda x: natural_key(str(x[0])))
    data_2021.sort(key=lambda x: natural_key(str(x[0])))

    data_2020.append(
        [
            'Total',
            sum(subl[1] for subl in data_2020),
            sum(subl[2] for subl in data_2020),
            sum(subl[3] for subl in data_2020),
            sum(subl[4] for subl in data_2020),
        ]
    )

    data_2021.append(
        [
            'Total',
            sum(subl[1] for subl in data_2021),
            sum(subl[2] for subl in data_2021),
            sum(subl[3] for subl in data_2021),
            sum(subl[4] for subl in data_2021),
        ]
    )

    # insert header
    data_2020.insert(0, header)
    data_2021.insert(0, header)

    return render_template(
        'reports/index.jinja2',
        data_2020=data_2020,
        data_2021=data_2021
    )


def ef_str_to_num(x):
    if x == 'NA':
        return 0
    if x == 'a':
        return 2
    if x == 'b':
        return 4
    if x == 'c':
        return 6
    if x == 'd':
        return 8
    if x == 'e':
        return 10
    if x == 'f':
        return 12
    if x == 'g':
        return 14
    if x == 'h':
        return 16
    if x == 'i':
        return 18
    if x == 'i+':
        return 19


def adult_avg(ac1, ac2, ac3):
    adult_div = 0
    if ac1 > 0:
        adult_div += 1
    if ac2 > 0:
        adult_div += 1
    if ac3 > 0:
        adult_div += 1
    if adult_div > 0:
        return (
            (ac1 + ac2 + ac3)/adult_div
        )
    else:
        return 0


def natural_key(string_):
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
