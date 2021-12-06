from flask import render_template, Blueprint
from flask_user import login_required
from app.models import site
from app.schemas import siteSchema
import datetime
import json

validation_blueprint = Blueprint('validation', __name__)

site_schema = siteSchema()


@validation_blueprint.route("/recorded_species_overlap")
@login_required
def recorded_species_overlap():
    site_data = json.loads(
        site_schema.jsonify(
            site.query.order_by(site.id).all(), many=True
        ).data
    )

    overlapped = [["Site", "Entry 1", "Entry 2"]]

    for s in site_data:
        recorded_species_list = []
        for survey in s['surveys']:
            for recorded_species in survey['recorded_species']:
                recorded_species_list.append(recorded_species)

        recorded_species_list = sorted(
                recorded_species_list, key=lambda i: i['species_id']
            )
        for i in range(len(recorded_species_list)):
            while i+1 < len(recorded_species_list) and \
                    recorded_species_list[i]['species_id'] == \
                    recorded_species_list[i+1]['species_id']:
                if (max(
                            datetime.datetime.fromisoformat(
                                recorded_species_list[i]['start']
                            ),
                            datetime.datetime.fromisoformat(
                                recorded_species_list[i+1]['start']
                            )
                        ) <=
                        min(
                            datetime.datetime.fromisoformat(
                                recorded_species_list[i]['end']
                            ),
                            datetime.datetime.fromisoformat(
                                recorded_species_list[i+1]['end']
                            )
                        )) or (datetime.datetime.fromisoformat(
                            recorded_species_list[i]['end']
                        ) ==
                        datetime.datetime.fromisoformat(
                            recorded_species_list[i+1]['end'])) \
                        or (datetime.datetime.fromisoformat(
                            recorded_species_list[i]['start']
                        ) ==
                        datetime.datetime.fromisoformat(
                            recorded_species_list[i+1]['start'])):
                    intermed1 = [
                        s["name"],
                        recorded_species_list[i],
                        recorded_species_list[i+1]
                    ]
                    intermed2 = [
                        s["name"],
                        recorded_species_list[i+1],
                        recorded_species_list[i]
                    ]
                    if not (
                            any(j == intermed1 for j in overlapped)
                            or any(j == intermed2 for j in overlapped)):
                        overlapped.append(
                            [
                                s["name"],
                                recorded_species_list[i],
                                recorded_species_list[i+1]
                            ]
                        )
                i += 1

    return render_template(
        'validation/recorded_speciees_overlap.jinja2',
        data=overlapped
    )
