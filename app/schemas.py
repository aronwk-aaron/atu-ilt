from app.models import (
    User,
    UserInvitation,
    site,
    survey,
    card as card_model,
    camera as camera_model,
    predator as predator_model,
    survey_camera_card,
    survey_predator,
    survey_predator_camera)
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class userSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = User
        include_relationships = False
        load_instance = True
        include_fk = True


class userInvitationSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = UserInvitation
        include_relationships = True
        load_instance = True
        include_fk = True

    invite_by_user = ma.Nested(userSchema)


class cameraSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = camera_model
        include_relationships = False
        load_instance = True
        include_fk = True


class cardSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = card_model
        include_relationships = False
        load_instance = True
        include_fk = True


class predatorSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = predator_model
        include_relationships = False
        load_instance = True
        include_fk = True


class surveyCameraSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey_camera_card
        include_relationships = True
        load_instance = True
        include_fk = True

    card_in = ma.Nested(cardSchema)
    card_out = ma.Nested(cardSchema)
    camera = ma.Nested(cameraSchema)


class surveyedPredatorSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey_predator
        include_relationships = True
        load_instance = True
        include_fk = True

    predator = ma.Nested(predatorSchema)


class recordedPredatorSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey_predator_camera
        include_relationships = True
        load_instance = True
        include_fk = True

    predator = ma.Nested(predatorSchema)


class surveySchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey
        include_relationships = True
        load_instance = True
        include_fk = True

    cameras = ma.Nested(surveyCameraSchema, many=True)
    surveyed_predators = ma.Nested(surveyedPredatorSchema, many=True)
    recorded_predators = ma.Nested(recordedPredatorSchema, many=True)


class siteSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = site
        include_relationships = True
        load_instance = True
        include_fk = True

    surveys = ma.Nested(surveySchema, many=True)
