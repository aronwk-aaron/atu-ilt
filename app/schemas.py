from app.models import (
    User,
    UserInvitation,
    site,
    survey,
    card as card_model,
    camera as camera_model,
    species as species_model,
    survey_camera_card,
    survey_species,
    survey_species_camera)
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


class specieschema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = species_model
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
        model = survey_species
        include_relationships = True
        load_instance = True
        include_fk = True

    species = ma.Nested(specieschema)


class recordedPredatorSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey_species_camera
        include_relationships = True
        load_instance = True
        include_fk = True

    species = ma.Nested(specieschema)


class surveySchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = survey
        include_relationships = True
        load_instance = True
        include_fk = True

    cameras = ma.Nested(surveyCameraSchema, many=True)
    surveyed_species = ma.Nested(surveyedPredatorSchema, many=True)
    recorded_species = ma.Nested(recordedPredatorSchema, many=True)


class siteSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = site
        include_relationships = True
        load_instance = True
        include_fk = True

    surveys = ma.Nested(surveySchema, many=True)
