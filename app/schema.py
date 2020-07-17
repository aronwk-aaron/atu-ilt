from flask_marshmallow.sqla import ModelSchema
from .models import (
    card,
    camera,
    site,
    predator,
    survey,
    survey_camera_card,
    survey_predator,
    survey_predator_camera
)

class cardSchema(ModelSchema):
    class Meta:
        model = card


class cameraSchema(ModelSchema):
    class Meta:
        model = camera


class siteSchema(ModelSchema):
    class Meta:
        model = site


class predatorSchema(ModelSchema):
    class Meta:
        model = predator


class surveySchema(ModelSchema):
    class Meta:
        model = survey


class survey_camera_cardSchema(ModelSchema):
    class Meta:
        model = survey_camera_card


class survey_predatorSchema(ModelSchema):
    class Meta:
        model = survey_predator


class survey_predator_cameraSchema(ModelSchema):
    class Meta:
        model = survey_predator_camera
