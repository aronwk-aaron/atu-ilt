from flask import render_template, Blueprint
from sqlalchemy.sql import func
from app.models import (
    site,
    survey,
    survey_camera_card,
    species,
    survey_species,
    survey_species_camera
)
from app.schemas import (
    siteSchema,
    surveySchema,
    surveyCameraSchema,
    recordedPredatorSchema,
    surveyedPredatorSchema,
    specieschema,
)
import json
import datetime
import collections

stats_blueprint = Blueprint('summary', __name__)

site_schema = siteSchema()
survey_schema = surveySchema()
species_schema = specieschema()
surveyed_species_schema = surveyedPredatorSchema()
recorded_species_schema = recordedPredatorSchema()
survey_camera_schema = surveyCameraSchema()


@stats_blueprint.route('/sites_2020')
def sites_2020():
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y20")).all(), many=True
        ).data
    )
    site_data = gen_site_data(sites)

    return render_template(
        'stats/sites.jinja2',
        data=site_data,
        year=2020
    )


@stats_blueprint.route('/sites_2021')
def sites_2021():
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y21")).all(), many=True
        ).data
    )
    site_data = gen_site_data(sites)

    return render_template(
        'stats/sites.jinja2',
        data=site_data,
        year=2021
    )


@stats_blueprint.route('/two_weeks_2020')
def two_weeks_2020():

    surveys = json.loads(
        survey_schema.jsonify(
            survey.query.order_by(survey.date).filter(survey.site.has(site.name.like("%Y20"))).all(), many=True
        ).data
    )

    survey_data = [
        gen_adult_survey_data(surveys, True),
        gen_nest_survey_data(surveys, True),
        gen_adult_survey_data(surveys, False),
        gen_nest_survey_data(surveys, False)
    ]
    return render_template(
        'stats/two_weeks.jinja2',
        survey_data=survey_data
    )


@stats_blueprint.route('/two_weeks_2021')
def two_weeks_2021():

    surveys = json.loads(
        survey_schema.jsonify(
            survey.query.order_by(survey.date).filter(survey.site.has(site.name.like("%Y21"))).all(), many=True
        ).data
    )

    survey_data = [
        gen_adult_survey_data(surveys, True),
        gen_nest_survey_data(surveys, True),
        gen_adult_survey_data(surveys, False),
        gen_nest_survey_data(surveys, False)
    ]
    return render_template(
        'stats/two_weeks.jinja2',
        survey_data=survey_data
    )


@stats_blueprint.route('/cameras_2020')
def cameras_2020():

    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y20")).all(), many=True
        ).data
    )
    survey_cameras = []
    for s in sites:
        for survey in s["surveys"]:
            survey_cameras.extend(survey["cameras"])

    survey_camera_data = gen_camera_data(survey_cameras)

    return render_template(
        'stats/cameras.jinja2',
        survey_camera_data=survey_camera_data,
        year=2020
    )


@stats_blueprint.route('/cameras_2021')
def cameras_2021():

    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y21")).all(), many=True
        ).data
    )
    survey_cameras = []
    for s in sites:
        for survey in s["surveys"]:
            survey_cameras.extend(survey["cameras"])

    survey_camera_data = gen_camera_data(survey_cameras)

    return render_template(
        'stats/cameras.jinja2',
        survey_camera_data=survey_camera_data,
        year=2021
    )


@stats_blueprint.route('/site_species_2020')
def site_species_2020():
    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y20")).all(), many=True
        ).data
    )

    data = gen_site_species_data(sites)

    return render_template(
        'stats/site_species.jinja2',
        data=data,
        year=2020
    )


@stats_blueprint.route('/site_species_2021')
def site_species_2021():

    sites = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).filter(site.name.like("%Y21")).all(), many=True
        ).data
    )

    data = gen_site_species_data(sites)

    return render_template(
        'stats/site_species.jinja2',
        data=data,
        year=2021
    )


@stats_blueprint.route('/species')
def species_route():
    species_data = gen_species_data()
    return render_template(
        'stats/species.jinja2',
        species_data=species_data
    )


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
            'nestingattempts': 0,
            'with_cameras': 0
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
            'nestingattempts': 0,
            'with_cameras': 0
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
            'nestingattempts': 0,
            'with_cameras': 0
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
        has_camera = False
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

            if 'cameras' in sites[s]['surveys'][i]:
                if (len(sites[s]['surveys'][i]['cameras']) > 0 and \
                        not has_camera):
                    data[sites[s]['loc_type'].replace('-', '_')]['with_cameras'] += 1
                    has_camera = True

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

        renest = 0
        if len(site_ef) > 0:
            for egg in range(len(site_ef)):
                site_ef[egg] = ef_str_to_num(site_ef[egg])
            # prime loop
            oos = 0
            yos = 0
            for egg in range(int(len(site_ef) / 4)):
                # we git rid of 0's since the are not useful
                curr_efs = list(
                    filter(lambda a: a, site_ef[egg * 4:4 + egg * 4]))
                if len(curr_efs) > 0:
                    ons = max(curr_efs)
                    yns = min(curr_efs)
                    if oos == 0 and yns > 0 and egg != 0:
                        # print("Re-nested")
                        renest += 1
                    elif abs(ons - yns) >= 6:
                        # print("Re-nested")
                        renest += 1
                    elif abs(ons - yos) >= 6:
                        # print("Re-nested")
                        renest += 1
                    elif yos >= 4 and yns > 0:
                        # print("Re-nested")
                        renest += 1
                    oos = max(curr_efs)
                    yos = min(curr_efs)
                else:
                    oos = 0
                    yos = 0
        data[sites[s]['loc_type'].replace(
            '-', '_')]['nestingattempts'] += renest
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


def ef_str_to_num(x):
    if x == 'NA':
        return 0
    if x == 'a':
        return 1
    if x == 'b':
        return 2
    if x == 'c':
        return 3
    if x == 'd':
        return 4
    if x == 'e':
        return 5
    if x == 'f':
        return 6
    if x == 'g':
        return 7
    if x == 'h':
        return 8
    if x == 'i':
        return 9
    if x == 'i+':
        return 10


def gen_adult_survey_data(surveys, de_dupe):
    data = [['Day', ' Adults', 'Fledgelings', 'Chicks', 'Eggs']]

    start_season_date = datetime.date.fromisoformat(surveys[0]["date"])
    end_season_date = datetime.date.fromisoformat(surveys[-1]["date"])
    current_season_date = datetime.date.fromisoformat(surveys[0]["date"])
    two_weeks = datetime.timedelta(days=14)
    one_day = datetime.timedelta(days=1)
    while current_season_date < end_season_date:

        end_itter_date = current_season_date + two_weeks
        tmp_surveys = []
        for surv in surveys:
            surv_date = datetime.date.fromisoformat(surv["date"])
            if surv_date < start_season_date or surv_date > end_season_date:
                continue  # not part of the season
            elif current_season_date <= surv_date < end_itter_date:
                tmp_surveys.append(
                    [
                        surv['site_id'],
                        adult_avg(surv['ac1'], surv['ac2'], surv['ac3']),
                        surv['fledgling'],
                        surv['chick02'] + surv['chick39'] + surv['chick1017'],
                        (
                            surv['egg1'] +
                            (surv['egg2'] * 2) +
                            (surv['egg3'] * 3)
                        )
                    ]
                )
        sort_sublist(tmp_surveys, 0)
        itter_data = [current_season_date, 0, 0, 0, 0]
        i = 0
        # print(f'Dedupe: {de_dupe}')
        while i < len(tmp_surveys):
            if de_dupe:
                # print('Find the one to keep')
                if (i + 1) < len(tmp_surveys):
                    while tmp_surveys[i][0] == tmp_surveys[i+1][0]:
                        # print(tmp_surveys[i])
                        # print(tmp_surveys[i+1])
                        # HERE IS THE PLACE
                        # to choose which one to drop
                        if tmp_surveys[i][1] > tmp_surveys[i+1][1]:
                            drop_survey = i + 1
                        elif tmp_surveys[i][1] < tmp_surveys[i+1][1]:
                            drop_survey = i
                        else:
                            if tmp_surveys[i][2] > tmp_surveys[i+1][2]:
                                drop_survey = i + 1
                            elif tmp_surveys[i][2] < tmp_surveys[i+1][2]:
                                drop_survey = i
                            else:
                                if tmp_surveys[i][3] > tmp_surveys[i+1][3]:
                                    drop_survey = i + 1
                                elif tmp_surveys[i][3] < tmp_surveys[i+1][3]:
                                    drop_survey = i
                                else:
                                    if tmp_surveys[i][4] > tmp_surveys[i+1][4]:
                                        drop_survey = i + 1
                                    elif tmp_surveys[i][4] < tmp_surveys[i+1][4]:
                                        drop_survey = i
                                    else:
                                        drop_survey = i

                        # if drop_survey == i:
                            # print("Dropped First")
                        # else:
                            # print("Dropped Second")
                        del tmp_surveys[drop_survey]
            itter_data[1] = itter_data[1] + tmp_surveys[i][1]
            itter_data[2] = itter_data[2] + tmp_surveys[i][2]
            itter_data[3] = itter_data[3] + tmp_surveys[i][3]
            itter_data[4] = itter_data[4] + tmp_surveys[i][4]

            i = i + 1
        # print("End Period")
        data.append(itter_data)
        current_season_date += one_day
    return data


def gen_nest_survey_data(surveys, de_dupe):
    data = [['Day', ' Adults', 'Fledgelings', 'Chicks', 'Nests']]

    start_season_date = datetime.date.fromisoformat(surveys[0]["date"])
    end_season_date = datetime.date.fromisoformat(surveys[-1]["date"])
    current_season_date = datetime.date.fromisoformat(surveys[0]["date"])
    two_weeks = datetime.timedelta(days=14)
    one_day = datetime.timedelta(days=1)
    while current_season_date < end_season_date:

        end_itter_date = current_season_date + two_weeks
        tmp_surveys = []
        for surv in surveys:
            surv_date = datetime.date.fromisoformat(surv["date"])
            if surv_date < start_season_date or surv_date > end_season_date:
                continue  # not part of the season
            elif current_season_date <= surv_date < end_itter_date:
                tmp_surveys.append(
                    [
                        surv['site_id'],
                        adult_avg(surv['ac1'], surv['ac2'], surv['ac3'], surv['egg1'] + surv['egg2'] + surv['egg3']),
                        surv['fledgling'],
                        surv['chick02'] + surv['chick39'] + surv['chick1017'],
                        (surv['egg1'] + surv['egg2'] + surv['egg3'])
                    ]
                )
        sort_sublist(tmp_surveys, 0)
        itter_data = [current_season_date, 0, 0, 0, 0]
        i = 0
        while i < len(tmp_surveys):
            if de_dupe:
                if (i + 1) < len(tmp_surveys):
                    while tmp_surveys[i][0] == tmp_surveys[i+1][0]:
                        # print(tmp_surveys[i])
                        # print(tmp_surveys[i+1])
                        # HERE IS THE PLACE
                        # to choose which one to drop
                        if tmp_surveys[i][1] > tmp_surveys[i+1][1]:
                            drop_survey = i + 1
                        elif tmp_surveys[i][1] < tmp_surveys[i+1][1]:
                            drop_survey = i
                        else:
                            if tmp_surveys[i][2] > tmp_surveys[i+1][2]:
                                drop_survey = i + 1
                            elif tmp_surveys[i][2] < tmp_surveys[i+1][2]:
                                drop_survey = i
                            else:
                                if tmp_surveys[i][3] > tmp_surveys[i+1][3]:
                                    drop_survey = i + 1
                                elif tmp_surveys[i][3] < tmp_surveys[i+1][3]:
                                    drop_survey = i
                                else:
                                    if tmp_surveys[i][4] > tmp_surveys[i+1][4]:
                                        drop_survey = i + 1
                                    elif tmp_surveys[i][4] < tmp_surveys[i+1][4]:
                                        drop_survey = i
                                    else:
                                        drop_survey = i

                        # if drop_survey == i:
                            # print("Dropped First")
                        # else:
                            # print("Dropped Second")
                        del tmp_surveys[drop_survey]
            itter_data[1] = itter_data[1] + tmp_surveys[i][1]
            itter_data[2] = itter_data[2] + tmp_surveys[i][2]
            itter_data[3] = itter_data[3] + tmp_surveys[i][3]
            itter_data[4] = itter_data[4] + tmp_surveys[i][4]

            i = i + 1
        # print("End Period")
        data.append(itter_data)
        current_season_date += one_day
    return data


def gen_camera_data(survey_cameras):
    data = {
        'time_recorded': datetime.timedelta(0),
        'no_time': 0,
        'failures': 0
    }

    for survey_camera in survey_cameras:
        if survey_camera['started_recording']:
            data['time_recorded'] += datetime.datetime.strptime(survey_camera['stopped_recording'], "%Y-%m-%dT%H:%M:%S") - \
                datetime.datetime.strptime(survey_camera['started_recording'], "%Y-%m-%dT%H:%M:%S")
        elif "setup" not in survey_camera["comment"].lower():
            data['no_time'] += 1

        if not survey_camera['functional']:
            data['failures'] += 1

    return data


def gen_site_species_data(sites):

    # 0: Site --> Table with site name
    # 1: OPSF --> number of species of observed species total at sandbar,
    # 2: RPSF --> number of species of recorded species total at sandbar,
    # 3: ODSF --> number of species of observed disturbed total at sandbar,
    # 4: RDSF --> number of species of recorded disturbers total at sandbar,
    # 5: Totlap --> total elapsed time of all species recorded on sandbar, ///// Sum of 6 and 7
    # 6: T_Pre_lap --> total elapsed time of just species on sandbar
    # 7: T_Dis_lap --> Total elapsed time of just disturbers on sandbar
    # 8: M_Pocc --> The species with the most reoccurences across time at sandbar
    # 9: M_Plap --> The species with the longest elapsed time at sandbar
    # 10: M_Pcnt --> The species with the highest summed count of individuals across time at the sandbar
    # 11: M_Docc --> The disturber with the most reoccurences across time at sandbar
    # 12: M_Dlap --> The disturber with the longest elapsed time at sandbar
    # 13: M_Dcnt --> The disturber with the highest summed count of individuals across time at the sandbar
    # 14: Cam_survey --> Count of how many surveys we have camera data for (count possible 0-4)
    # 15: SD_cards_out --> number of SD cards take out (count possible 0-8)
    # 16: Camlap --> Total elapsed time for cameras on this site
    # 17: T_Pre_cnt
    # 18: T_Pre_occ
    # 19: T_Dis_cnt
    # 20: T_Dis_occ
    # ------ Classification
    # 21: C_Mam_lap
    # 22: C_Mam_cnt
    # 23: C_Mam_occ
    # 24: C_Avi_lap
    # 25: C_Avi_cnt
    # 26: C_Avi_occ
    # 27: C_Hum_lap
    # 28: C_Hum_cnt
    # 29: C_Hum_occ
    # 30: C_Rep_lap
    # 31: C_Rep_cnt
    # 32: C_Rep_occ
    # 33: C_Env_lap
    # 34: C_Env_cnt
    # 35: C_Env_occ
    # 36: C_Oth_lap
    # 37: C_Oth_cnt
    # 38: C_Oth_occ
    # ------ Risk
    # 39: R_Hig_lap
    # 40: R_Hig_cnt
    # 41: R_Hig_occ
    # 42: R_Low_lap
    # 43: R_Low_cnt
    # 44: R_Low_occ
    # 45: R_Non_lap
    # 46: R_Non_cnt
    # 47: R_Non_occ
    # ------ Group
    # 48: G_Her_lap
    # 49: G_Her_cnt
    # 50: G_Her_occ
    # 51: G_Hum_lap
    # 52: G_Hum_cnt
    # 53: G_Hum_occ
    # 54: G_Mes_lap
    # 55: G_Mes_cnt
    # 56: G_Mes_occ
    # 57: G_Rap_lap
    # 58: G_Rap_cnt
    # 59: G_Rap_occ
    # 60: G_Sho_lap
    # 61: G_Sho_cnt
    # 62: G_Sho_occ
    # 63: G_SMa_lap
    # 64: G_SMa_cnt
    # 65: G_SMa_occ
    # 66: G_Son_lap
    # 67: G_Son_cnt
    # 68: G_Son_occ
    # 69: G_Tra_lap
    # 70: G_Tra_cnt
    # 71: G_Tra_occ
    # 72: G_Wad_lap
    # 73: G_Wad_cnt
    # 74: G_Wad_occ
    # 75: G_Wat_lap
    # 76: G_Wat_cnt
    # 77: G_Wat_occ

    data = [
        [
            "Site",
            "OPSF",
            "RPSF",
            "ODSF",
            "RDSF",
            "Totlap",
            "Plap",
            "Dlap",
            "M_Pocc",
            "M_Plap",
            "M_Pcnt",
            "M_Docc",
            "M_Dlap",
            "M_Dcnt",
            "Cam_survey",
            "SD_cards_out",
            "Camlap",
            "T_Pre_cnt",
            "T_Pre_occ",
            "T_Dis_cnt",
            "T_Dis_occ",
            "C_Mam_lap",
            "C_Mam_cnt",
            "C_Mam_occ",
            "C_Avi_lap",
            "C_Avi_cnt",
            "C_Avi_occ",
            "C_Hum_lap",
            "C_Hum_cnt",
            "C_Hum_occ",
            "C_Rep_lap",
            "C_Rep_cnt",
            "C_Rep_occ",
            "C_Env_lap",
            "C_Env_cnt",
            "C_Env_occ",
            "C_Oth_lap",
            "C_Oth_cnt",
            "C_Oth_occ",
            "R_Hig_lap",
            "R_Hig_cnt",
            "R_Hig_occ",
            "R_Low_lap",
            "R_Low_cnt",
            "R_Low_occ",
            "R_Non_lap",
            "R_Non_cnt",
            "R_Non_occ",
            "G_Her_lap",
            "G_Her_cnt",
            "G_Her_occ",
            "G_Hum_lap",
            "G_Hum_cnt",
            "G_Hum_occ",
            "G_Mes_lap",
            "G_Mes_cnt",
            "G_Mes_occ",
            "G_Rap_lap",
            "G_Rap_cnt",
            "G_Rap_occ",
            "G_Sho_lap",
            "G_Sho_cnt",
            "G_Sho_occ",
            "G_SMa_lap",
            "G_SMa_cnt",
            "G_SMa_occ",
            "G_Son_lap",
            "G_Son_cnt",
            "G_Son_occ",
            "G_Tra_lap",
            "G_Tra_cnt",
            "G_Tra_occ",
            "G_Wad_lap",
            "G_Wad_cnt",
            "G_Wad_occ",
            "G_Wat_lap",
            "G_Wat_cnt",
            "G_Wat_occ",
        ]
    ]

    for site in sites:
        entry = [
            site["name"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #noqa
        site_surveyed_predator = []
        site_recorded_predator = []
        site_surveyed_disturbers = []
        site_recorded_disturbers = []

        # only by camera data
        # --- Classification
        site_c_mam = []
        site_c_avi = []
        site_c_hum = []
        site_c_rep = []
        site_c_env = []
        site_c_oth = []
        # --- Risk
        site_r_non = []
        site_r_hig = []
        site_r_low = []
        # --- Group
        site_g_her = []
        site_g_hum = []
        site_g_mes = []
        site_g_rap = []
        site_g_sho = []
        site_g_sma = []
        site_g_son = []
        site_g_tra = []
        site_g_wad = []
        site_g_wat = []

        # Get the data we need gathered in one list to more easily interate through it
        for survey in site["surveys"]:
            if len(survey["cameras"]) > 0:
                entry[14] += 1
            for camera in survey["cameras"]:
                if camera["stopped_recording"]:
                    entry[16] += (
                        datetime.datetime.fromisoformat(camera["stopped_recording"]) -
                        datetime.datetime.fromisoformat(camera["started_recording"])
                    ).total_seconds()
            for survey_camera in survey["cameras"]:
                if survey_camera["card_out"]["name"] != "None":
                    entry[15] += 1
            for recorded_species in survey["recorded_species"]:
                if recorded_species["species"]["species_type"] == "predator":
                    site_recorded_predator.append(recorded_species)
                else:
                    site_recorded_disturbers.append(recorded_species)
                # --- Classification
                if recorded_species['species']['classification'] == 'mammal':
                    site_c_mam.append(recorded_species)
                elif recorded_species['species']['classification'] == 'avian':
                    site_c_avi.append(recorded_species)
                elif recorded_species['species']['classification'] == 'human':
                    site_c_hum.append(recorded_species)
                elif recorded_species['species']['classification'] == 'reptile':
                    site_c_rep.append(recorded_species)
                elif recorded_species['species']['classification'] == 'environmental':
                    site_c_env.append(recorded_species)
                else:
                    site_c_oth.append(recorded_species)
                # --- Risk
                if recorded_species['species']['risk'] == 'high':
                    site_r_hig.append(recorded_species)
                elif recorded_species['species']['risk'] == 'low':
                    site_r_low.append(recorded_species)
                else:
                    site_r_non.append(recorded_species)
                # --- Group
                if recorded_species['species']['group'] == 'herp':
                    site_g_her.append(recorded_species)
                elif recorded_species['species']['group'] == 'human':
                    site_g_hum.append(recorded_species)
                elif recorded_species['species']['group'] == 'meso':
                    site_g_mes.append(recorded_species)
                elif recorded_species['species']['group'] == 'raptor':
                    site_g_rap.append(recorded_species)
                elif recorded_species['species']['group'] == 'shorebird':
                    site_g_sho.append(recorded_species)
                elif recorded_species['species']['group'] == 'smammal':
                    site_g_sma.append(recorded_species)
                elif recorded_species['species']['group'] == 'songbird':
                    site_g_son.append(recorded_species)
                elif recorded_species['species']['group'] == 'trampler':
                    site_g_tra.append(recorded_species)
                elif recorded_species['species']['group'] == 'wader':
                    site_g_wad.append(recorded_species)
                else:
                    site_g_wat.append(recorded_species)
            for surveyed_species in survey["surveyed_species"]:
                if surveyed_species["species"]["species_type"] == "predator":
                    site_surveyed_predator.append(surveyed_species)
                else:
                    site_surveyed_disturbers.append(surveyed_species)

        # collects will get the count of each unique entry, i just want the number of unique entries
        entry[1] = len(collections.Counter(c["species"]["species"] for c in site_surveyed_predator))
        entry[2] = len(collections.Counter(c["species"]["species"] for c in site_recorded_predator))
        entry[3] = len(collections.Counter(c["species"]["species"] for c in site_surveyed_disturbers))
        entry[4] = len(collections.Counter(c["species"]["species"] for c in site_recorded_disturbers))

        # magic lambda functions
        entry[6] = round(sum(map(lambda x: time_difference(x), site_recorded_predator))/3600, 2)
        entry[7] = round(sum(map(lambda x: time_difference(x), site_recorded_disturbers))/3600, 2)

        entry[5] = round(entry[6] + entry[7], 2)

        new_pred_list = collections.Counter(c["species"]["species"] for c in site_recorded_predator).most_common()
        entry[8] = (f"{new_pred_list[0][0]}: {new_pred_list[0][1]}" if len(new_pred_list) > 0 else None)

        pred_list = list(collections.Counter(c["species"]["species"] for c in site_recorded_predator).keys())
        time_dict = {}
        for pred in pred_list:
            time_dict[pred] = sum(map(lambda x: time_difference(x) if (x["species"]["species"] == pred) else 0, site_recorded_predator))
        entry[9] = max(time_dict.items(), key=lambda x: x[1]) if (len(time_dict) > 0) else "None"
        if entry[9] != "None":
            entry[9] = f"{entry[9][0]}: {round(entry[9][1]/3600, 2)}"

        count_dict = {}
        for pred in pred_list:
            count_dict[pred] = sum(
                map(lambda x: x["count"] if (x["species"]["species"] == pred) else 0, site_recorded_predator))
            count_dict[pred] += sum(
                map(lambda x: x["count"] if (x["species"]["species"] == pred) else 0, site_surveyed_predator))
        entry[10] = max(count_dict.items(), key=lambda x: x[1]) if (len(count_dict) > 0) else "None"
        if entry[10] != "None":
            entry[10] = f"{entry[10][0]}: {entry[10][1]}"

        new_dist_list = collections.Counter(c["species"]["species"] for c in site_recorded_disturbers).most_common()
        entry[11] = (f"{new_dist_list[0][0]}: { new_dist_list[0][1]}" if len(new_dist_list) > 0 else None)

        dist_list = list(collections.Counter(c["species"]["species"] for c in site_recorded_disturbers).keys())
        time_dict = {}
        for dist in dist_list:
            time_dict[dist] = sum(map(lambda x: time_difference(x) if (x["species"]["species"] == dist) else 0, site_recorded_disturbers))
        entry[12] = max(time_dict.items(), key=lambda x: x[1]) if (len(time_dict) > 0) else "None"
        if entry[12] != "None":
            entry[12] = f"{entry[12][0]}: {round(entry[12][1]/3600, 2)}"

        count_dict = {}
        for dist in dist_list:
            count_dict[dist] = sum(
                map(lambda x: x["count"]if (x["species"]["species"] == dist) else 0, site_recorded_disturbers))
            count_dict[dist] += sum(
                map(lambda x: x["count"]if (x["species"]["species"] == dist) else 0, site_surveyed_disturbers))
        entry[13] = max(count_dict.items(), key=lambda x: x[1]) if (len(count_dict) > 0) else "None"
        if entry[13] != "None":
            entry[13] = f"{entry[13][0]}: {entry[13][1]}"

        entry[16] = round(entry[16]/3600, 2)

        entry[17] = sum(map(lambda x: x["count"], site_recorded_predator))
        entry[18] = len(site_recorded_predator)
        entry[19] = sum(map(lambda x: x["count"], site_recorded_disturbers))
        entry[20] = len(site_recorded_disturbers)
        entry[21] = round(sum(map(lambda x: time_difference(x), site_c_mam))/3600, 2)
        entry[22] = sum(map(lambda x: x["count"], site_c_mam))
        entry[23] = len(site_c_mam)
        entry[24] = round(sum(map(lambda x: time_difference(x), site_c_avi))/3600, 2)
        entry[25] = sum(map(lambda x: x["count"], site_c_avi))
        entry[26] = len(site_c_avi)
        entry[27] = round(sum(map(lambda x: time_difference(x), site_c_hum))/3600, 2)
        entry[28] = sum(map(lambda x: x["count"], site_c_hum))
        entry[29] = len(site_c_hum)
        entry[30] = round(sum(map(lambda x: time_difference(x), site_c_rep))/3600, 2)
        entry[31] = sum(map(lambda x: x["count"], site_c_rep))
        entry[32] = len(site_c_rep)
        entry[33] = round(sum(map(lambda x: time_difference(x), site_c_env))/3600, 2)
        entry[34] = sum(map(lambda x: x["count"], site_c_env))
        entry[35] = len(site_c_env)
        entry[36] = round(sum(map(lambda x: time_difference(x), site_c_oth))/3600, 2)
        entry[37] = sum(map(lambda x: x["count"], site_c_oth))
        entry[38] = len(site_c_oth)
        entry[39] = round(sum(map(lambda x: time_difference(x), site_r_non))/3600, 2)
        entry[40] = sum(map(lambda x: x["count"], site_r_non))
        entry[41] = len(site_r_non)
        entry[42] = round(sum(map(lambda x: time_difference(x), site_r_hig))/3600, 2)
        entry[43] = sum(map(lambda x: x["count"], site_r_hig))
        entry[44] = len(site_r_hig)
        entry[45] = round(sum(map(lambda x: time_difference(x), site_r_low))/3600, 2)
        entry[46] = sum(map(lambda x: x["count"], site_r_low))
        entry[47] = len(site_r_low)
        entry[48] = round(sum(map(lambda x: time_difference(x), site_g_her))/3600, 2)
        entry[49] = sum(map(lambda x: x["count"], site_g_her))
        entry[50] = len(site_g_her)
        entry[51] = round(sum(map(lambda x: time_difference(x), site_g_hum))/3600, 2)
        entry[52] = sum(map(lambda x: x["count"], site_g_hum))
        entry[53] = len(site_g_hum)
        entry[54] = round(sum(map(lambda x: time_difference(x), site_g_mes))/3600, 2)
        entry[55] = sum(map(lambda x: x["count"], site_g_mes))
        entry[56] = len(site_g_mes)
        entry[57] = round(sum(map(lambda x: time_difference(x), site_g_rap))/3600, 2)
        entry[58] = sum(map(lambda x: x["count"], site_g_rap))
        entry[59] = len(site_g_rap)
        entry[60] = round(sum(map(lambda x: time_difference(x), site_g_sho))/3600, 2)
        entry[61] = sum(map(lambda x: x["count"], site_g_sho))
        entry[62] = len(site_g_sho)
        entry[63] = round(sum(map(lambda x: time_difference(x), site_g_sma))/3600, 2)
        entry[64] = sum(map(lambda x: x["count"], site_g_sma))
        entry[65] = len(site_g_sma)
        entry[66] = round(sum(map(lambda x: time_difference(x), site_g_son))/3600, 2)
        entry[67] = sum(map(lambda x: x["count"], site_g_son))
        entry[68] = len(site_g_son)
        entry[69] = round(sum(map(lambda x: time_difference(x), site_g_tra))/3600, 2)
        entry[70] = sum(map(lambda x: x["count"], site_g_tra))
        entry[71] = len(site_g_tra)
        entry[72] = round(sum(map(lambda x: time_difference(x), site_g_wad))/3600, 2)
        entry[73] = sum(map(lambda x: x["count"], site_g_wad))
        entry[74] = len(site_g_wad)
        entry[75] = round(sum(map(lambda x: time_difference(x), site_g_wat))/3600, 2)
        entry[76] = sum(map(lambda x: x["count"], site_g_wat))
        entry[77] = len(site_g_wat)

        # normalize the number of cameras,
        # since there will be an exit entry that's counted,
        # but shouldn't be counted
        if entry[14] > 0:
            entry[14] -= 1
        data.append(entry)

    return data


def gen_species_data():
    data = {
        'surveyed_prevalence': [],
        'recorded_prevalence': [],
        'surveyed_abundance': [],
        'recorded_abundance': [],
        'recorded_duration': []
    }

    species_data = json.loads(
        species_schema.jsonify(
            species.query.order_by(species.species).all(), many=True
        ).data
    )

    for p in species_data:  # surveyed
        surveyed_prevalence = survey_species.query.filter(
                p['id'] == survey_species.species_id
            ).count()
        data['surveyed_prevalence'].append(
            (p['species'], surveyed_prevalence)
        )
        surveyed_abundance = json.loads(
            surveyed_species_schema.jsonify(
                survey_species.query.filter(
                    p['id'] == survey_species.species_id
                ).all(), many=True
            ).data
        )
        data['surveyed_abundance'].append(
            (
                p['species'],
                sum(map(lambda x: int(x['count']), surveyed_abundance))
            )
        )

        # recorded
        recorded_prevalence = survey_species_camera.query.filter(
                p['id'] == survey_species_camera.species_id
            ).count()
        data['recorded_prevalence'].append(
            (p['species'], recorded_prevalence)
        )

        recorded_abundance = json.loads(
            recorded_species_schema.jsonify(
                survey_species_camera.query.filter(
                    p['id'] == survey_species_camera.species_id
                ).all(), many=True
            ).data
        )
        data['recorded_abundance'].append(
            (
                p['species'],
                sum(map(lambda x: int(x['count']), recorded_abundance))
            )
        )
        data['recorded_duration'].append(
            [
                p['species'],
                sum(map(lambda x: time_difference(x), recorded_abundance))
            ]
        )

    sort_sublist(data['surveyed_prevalence'])
    sort_sublist(data['recorded_prevalence'])
    sort_sublist(data['surveyed_abundance'])
    sort_sublist(data['recorded_abundance'])
    sort_sublist(data['recorded_duration'])

    # convert seconds to hours
    for item in range(len(data['recorded_duration'])):
        # print(data['recorded_duration'][item][1])
        data['recorded_duration'][item][1] = round(
            data['recorded_duration'][item][1]/3600, 1
        )

    data['surveyed_prevalence'].reverse()
    data['recorded_prevalence'].reverse()
    data['surveyed_abundance'].reverse()
    data['recorded_abundance'].reverse()
    data['recorded_duration'].reverse()

    del data['surveyed_prevalence'][5:]
    del data['recorded_prevalence'][5:]
    del data['surveyed_abundance'][5:]
    del data['recorded_abundance'][5:]
    del data['recorded_duration'][5:]
    # print(data['recorded_duration'])
    return data


def time_difference(x):
    difference = (
        datetime.datetime.fromisoformat(x["end"]) -
        datetime.datetime.fromisoformat(x["start"])
    )
    # if time is within the same minute, make it 30 seconds
    difference = difference.total_seconds()

    return difference


def sort_sublist(sub_li, index=1):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[index])
    return sub_li


def adult_avg(ac1, ac2, ac3, nests=0):
    if nests > 0:
        return nests * 2
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
