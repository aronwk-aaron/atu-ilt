from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserMixin

import logging
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import OperationalError, StatementError
from time import sleep


class RetryingQuery(BaseQuery):
    __retry_count__ = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "server closed the connection unexpectedly" not in str(ex):
                    raise
                if attempts < self.__retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    logging.error(
                        "Database connection error: {} - sleeping for {}s"
                        " and will retry (attempt #{} of {})".format(
                            ex, sleep_for, attempts, self.__retry_count__
                        )
                    )
                    sleep(sleep_for)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not \
                        in str(ex):
                    raise
                self.session.rollback()


db = SQLAlchemy(query_class=RetryingQuery)
migrate = Migrate()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='1'
    )

    email = db.Column(
        db.Unicode(255),
        nullable=False,
        server_default=u'',
        unique=True
    )
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(
        db.String(100), nullable=False, server_default=''
    )
    last_name = db.Column(
        db.String(100), nullable=False, server_default=''
    )

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def get_user_by_id(*, user_id=None):
        return User.query.filter(user_id == User.id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query \
            .join(UsersRoles, User.id == UsersRoles.user_id) \
            .add_columns(User.id, User.first_name, User.last_name, User.email,
                         UsersRoles.role_id) \
            .filter(User.id == UsersRoles.user_id) \
            .filter(UsersRoles.user_id == User.id) \
            .all()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(
        db.String(50), nullable=False, server_default=u'', unique=True
    )  # for @roles_accepted()


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')
    )
    role_id = db.Column(
        db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE')
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update_userrole(*, user_id=None, role_id=None):
        user = UsersRoles.query.filter(user_id == UsersRoles.user_id).first()
        user.role_id = role_id

        user.save()


class UserInvitation(db.Model):
    __tablename__ = 'user_invite'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    # save the user of the invitee
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # token used for registration page to identify user registering
    token = db.Column(db.String(100), nullable=False, server_default='')
    invited_by_user = db.relationship('User')

    @staticmethod
    def get_user_by_id(*, user_id=None):
        return User.query.filter(user_id == User.id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    card_in = db.relationship(
        'survey_camera_card',
        primaryjoin="or_(card.id==survey_camera_card.card_in_id)",
        back_populates="card_in"
    )
    card_out = db.relationship(
        'survey_camera_card',
        primaryjoin="or_(card.id==survey_camera_card.card_out_id)",
        back_populates="card_out"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class camera(db.Model):
    __tablename__ = 'cameras'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    functional = db.Column(db.Boolean, default=True, nullable=False)
    comment = db.Column(db.String(1024))
    survey_camera = db.relationship(
        'survey_camera_card',
        back_populates="camera"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    loc_type = db.Column(db.String(255), nullable=False)
    elev = db.Column(db.Float, nullable=False)

    snag_perch = db.Column(db.Integer, nullable=False)

    psub = db.Column(db.String(50), nullable=False)
    perc_psub = db.Column(db.Integer, nullable=False)
    silt_clay = db.Column(db.Boolean, nullable=False)
    sand = db.Column(db.Boolean, nullable=False)
    gravel = db.Column(db.Boolean, nullable=False)
    sm_rocks = db.Column(db.Boolean, nullable=False)

    est_area = db.Column(db.Float)
    length = db.Column(db.Float)
    perimeter = db.Column(db.Boolean)
    perimeter_length = db.Column(db.Float)
    mainland_distance = db.Column(db.Float)
    comment = db.Column(db.String(1024))

    surveys = db.relationship('survey', order_by='survey.date')

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class species(db.Model):
    __tablename__ = 'species'

    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(255), nullable=False)
    species_type = db.Column(db.String(255), nullable=False)
    risk = db.Column(db.String(255), nullable=True)
    classification = db.Column(db.String(255), nullable=True)
    group = db.Column(db.String(255), nullable=True)

    survey_species = db.relationship(
        'survey_species',
        back_populates="species"
    )
    recorded_species = db.relationship(
        'survey_species_camera',
        back_populates="species"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)

    site_id = db.Column(
        db.Integer(),
        db.ForeignKey(site.id),
        nullable=False
    )
    site = db.relationship('site')

    date = db.Column(db.Date(), nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    time_in = db.Column(db.Time(), nullable=False)
    time_out = db.Column(db.Time(), nullable=False)
    surveyed = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(50), nullable=False)

    ac1 = db.Column(db.Integer, nullable=False)
    ac2 = db.Column(db.Integer, nullable=False)
    ac3 = db.Column(db.Integer, nullable=False)

    egg1 = db.Column(db.Integer, nullable=False)
    egg2 = db.Column(db.Integer, nullable=False)
    egg3 = db.Column(db.Integer, nullable=False)

    chick02 = db.Column(db.Integer, nullable=False)
    chick39 = db.Column(db.Integer, nullable=False)
    chick1017 = db.Column(db.Integer, nullable=False)
    fledgling = db.Column(db.Integer, nullable=False)

    ef1 = db.Column(db.String(3), nullable=False)
    ef2 = db.Column(db.String(3), nullable=False)
    ef3 = db.Column(db.String(3), nullable=False)
    ef4 = db.Column(db.String(3), nullable=False)

    scrape = db.Column(db.Boolean, nullable=False)

    pveg = db.Column(db.String(50), nullable=False)
    perc_pveg = db.Column(db.Integer, nullable=False)
    size_type = db.Column(db.String(255), nullable=False)

    cwdn1 = db.Column(db.Integer, nullable=False)
    cwdn2 = db.Column(db.Integer, nullable=False)
    cwdn3 = db.Column(db.Integer, nullable=False)
    cwdlog = db.Column(db.Integer, nullable=False)

    w_temp = db.Column(db.Float)
    a_temp = db.Column(db.Float)
    perc_dio = db.Column(db.Float)
    sal = db.Column(db.Float)
    sp_condu = db.Column(db.Float)
    condu = db.Column(db.Float)

    comment = db.Column(db.String(1024))

    cameras = db.relationship('survey_camera_card')
    surveyed_species = db.relationship('survey_species')
    recorded_species = db.relationship('survey_species_camera')

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class survey_camera_card(db.Model):
    __tablename__ = 'survey_camera_card'

    survey_id = db.Column(
        db.Integer(),
        db.ForeignKey(survey.id),
        primary_key=True
    )

    camera_id = db.Column(
        db.Integer(),
        db.ForeignKey(camera.id),
        primary_key=True
    )

    camera = db.relationship('camera')

    card_in_id = db.Column(
        db.Integer,
        db.ForeignKey(card.id)
    )
    card_in = db.relationship('card', foreign_keys=[card_in_id])

    card_out_id = db.Column(
        db.Integer,
        db.ForeignKey(card.id)
    )
    card_out = db.relationship('card', foreign_keys=[card_out_id])
    cleared = db.Column(db.Boolean, nullable=False)
    ch_bat = db.Column(db.Boolean, nullable=False)
    started_recording = db.Column(db.DateTime(), nullable=True)
    stopped_recording = db.Column(db.DateTime(), nullable=True)
    functional = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.String(1024))

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class survey_species(db.Model):
    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(survey.id),
        primary_key=True
    )
    survey = db.relationship('survey')
    species_id = db.Column(
        db.Integer,
        db.ForeignKey(species.id),
        primary_key=True
    )
    species = db.relationship('species')

    tracks = db.Column(db.Boolean)
    sighting = db.Column(db.Boolean)
    scat = db.Column(db.Boolean)
    adult_mort = db.Column(db.Boolean)
    chick_mort = db.Column(db.Boolean)
    nest_dest = db.Column(db.Boolean)
    count = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1024))

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class survey_species_camera(db.Model):
    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(survey.id),
        primary_key=True
    )
    survey = db.relationship('survey')
    species_id = db.Column(
        db.Integer,
        db.ForeignKey(species.id),
        primary_key=True
    )
    species = db.relationship('species')

    start = db.Column(
        db.DateTime(),
        primary_key=True
    )
    end = db.Column(
        db.DateTime(),
        primary_key=True
    )
    count = db.Column(db.Integer, nullable=False)
    scat = db.Column(db.Boolean, nullable=False)
    adult_mort = db.Column(db.Boolean, nullable=False)
    chick_mort = db.Column(db.Boolean, nullable=False)
    nest_dest = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.String(1024))

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
