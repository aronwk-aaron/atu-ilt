from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


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
    comment = db.Column(db.String(1024))

    survey = db.relationship('survey', back_populates="site")

    def save(self):
        db.session.add(self)
        db.session.commit()


class predator(db.Model):
    __tablename__ = 'predators'

    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(255), nullable=False)
    predator_type = db.Column(db.String(255), nullable=False)
    volatility = db.Column(db.Integer)
    survey_predator = db.relationship(
        'survey_predator',
        back_populates="predator"
    )
    recorded_predator = db.relationship(
        'survey_predator_camera',
        back_populates="predator"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()


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

    def save(self):
        db.session.add(self)
        db.session.commit()


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
    functional = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.String(1024))

    def save(self):
        db.session.add(self)
        db.session.commit()


class survey_predator(db.Model):
    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(survey.id),
        primary_key=True
    )
    predator_id = db.Column(
        db.Integer,
        db.ForeignKey(predator.id),
        primary_key=True
    )
    predator = db.relationship('predator')
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


class survey_predator_camera(db.Model):
    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(survey.id),
        primary_key=True
    )
    predator_id = db.Column(
        db.Integer,
        db.ForeignKey(predator.id),
        primary_key=True
    )
    predator = db.relationship('predator')

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
