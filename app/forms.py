from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    BooleanField,
    HiddenField,
    TextAreaField,
    SubmitField
)

from wtforms.fields.html5 import (
    IntegerField,
    DateField,
    TimeField,
    DateTimeLocalField,
    DecimalField
)

from wtforms.validators import (
    DataRequired,
    InputRequired,
    NumberRange,
    Optional
)


class camera_form(FlaskForm):
    name = StringField(
        label='Name',
        validators=[
            DataRequired()
        ]
    )
    brand = SelectField(
        label='Brand',
        choices=[
            ('browning', 'Browning'),
            ('spypoint', 'SpyPoint'),
        ],
        validators=[
            DataRequired()
        ]
    )
    functional = BooleanField(
        label='Is/was the camera functional?',
        default=False
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()


class card_form(FlaskForm):
    name = StringField(
        label='Name',
        validators=[
            DataRequired()
        ]
    )
    size = SelectField(
        label='Size',
        coerce=int,
        choices=[
            (16, '16GB'),
            (32, '32GB'),
            (64, '64GB'),
            (128, '128GB'),
        ],
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField()


class site_form(FlaskForm):
    name = StringField(
        label='Name',
        validators=[
            DataRequired()
        ]
    )
    loc_type = SelectField(
        label='Location Type',
        choices=[
            ('rooftop', 'Rooftop'),
            ('sandbar-island', 'Island - Sandbar'),
            ('sandbar-main', 'Main - Sandbar'),
        ],
        validators=[
            DataRequired()
        ]
    )
    size_type = SelectField(
        label='Size',
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large')
        ],
        validators=[
            DataRequired()
        ]
    )
    elevation = DecimalField(
        label='Elevation'
    )
    snag_perch = IntegerField(
        label='Snag/Perch Count',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    substrate_choices = [
        ('silt_clay', 'Silt/Clay'),
        ('gravel', 'Gravel'),
        ('sand', 'Sand'),
        ('sm_rocks', 'Small Rocks'),
    ]
    primary_substrate = SelectField(
        label='Primary Substrate',
        choices=substrate_choices,
        validators=[
            DataRequired()
        ]
    )
    precentage_primary_substrate = IntegerField(
        label='Precentage Primary Substrate',
        default=0,
        validators=[
            NumberRange(min=0, max=100),
            DataRequired()
        ]
    )
    silt_clay = BooleanField(
        label='Silt/Clay Presence'
    )
    sand = BooleanField(
        label='Sand Presence'
    )
    gravel = BooleanField(
        label='Gravel Presence'
    )
    sm_rocks = BooleanField(
        label='Small Rocks Presence'
    )
    est_area = DecimalField(
        label='Estimated Area',
        validators=[
            Optional(),
        ]
    )
    length = DecimalField(
        label='Length',
        validators=[
            Optional(),
        ]
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()


class predator_form(FlaskForm):
    species = StringField(
        label='Species',
        validators=[
            DataRequired()
        ]
    )
    predator_type = SelectField(
        label='Type',
        choices=[
            ('mammal', 'Mammal'),
            ('avian', 'Avian'),
            ('human', 'Human'),
            ('reptile', 'Reptile'),
            ('other', 'Other'),
        ],
        validators=[
            DataRequired()
        ]
    )
    volatility = IntegerField(
        label='Volatility',
        validators=[
            Optional(),
            NumberRange(min=0, max=10),
        ]
    )
    submit = SubmitField()


class survey_form(FlaskForm):
    site = SelectField(
        label='Site',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    date = DateField(
        label='Date',
        validators=[
            DataRequired()
        ]
    )
    crew = IntegerField(
        label='Crew Count',
        validators=[
            NumberRange(min=1, max=6),
            DataRequired()
        ]
    )
    time_in = TimeField(
        label='Time In',
        validators=[
            DataRequired()
        ]
    )
    time_out = TimeField(
        label='Time Out',
        validators=[
            DataRequired()
        ]
    )
    precentage_surveyed = IntegerField(
        label='Precentage Surveyed',
        default=0,
        validators=[
            NumberRange(min=0, max=100),
            DataRequired()
        ]
    )
    method = SelectField(
        label='Method',
        choices=[
            ('foot', 'Foot'),
            ('boat', 'Boat'),
            ('peeking', 'Peeking'),
        ],
        validators=[
            DataRequired()
        ]
    )
    ac1 = IntegerField(
        label='Adult Tern Count 1',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    ac2 = IntegerField(
        label='Adult Tern Count 2',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    ac3 = IntegerField(
        label='Adult Tern Count 3',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    egg1 = IntegerField(
        label='Nest(s) with 1 Egg',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    egg2 = IntegerField(
        label='Nest(s) with 2 Egg',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    egg3 = IntegerField(
        label='Nest(s) with 3 Egg',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    scrape = BooleanField(
        label='Scrape Presence'
    )
    chick02 = IntegerField(
        label='Chicks 0-2 day(s) old',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    chick39 = IntegerField(
        label='Chicks 3-9 days old',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    chick1017 = IntegerField(
        label='Chicks 10-17 days old',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    fledgling = IntegerField(
        label='Fledglings',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    ef_choices = [
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
        ('e', 'e'),
        ('f', 'f'),
        ('g', 'g'),
        ('h', 'h'),
        ('i', 'i'),
        ('i+', 'i+'),
    ]
    ef1 = SelectField(
        label='Egg Float #1',
        choices=ef_choices
    )
    ef2 = SelectField(
        label='Egg Float #2',
        choices=ef_choices
    )
    ef3 = SelectField(
        label='Egg Float #3',
        choices=ef_choices
    )
    ef4 = SelectField(
        label='Egg Float #4',
        choices=ef_choices
    )
    ef_com = TextAreaField(
        label='Egg Float Comments'
    )
    vegetation_choices = [
        ('grass', 'Grass'),
        ('herb', 'Herb'),
        ('vine', 'Vine'),
        ('woody', 'Woody'),
        ('treey', 'Treey'),
    ]
    primary_vegitation = SelectField(
        label='Primary Vegetation',
        choices=vegetation_choices,
        validators=[
            DataRequired()
        ]
    )
    precentage_primary_vegitation = IntegerField(
        label='Precentage Vegetation',
        default=0,
        validators=[
            NumberRange(min=0, max=100),
            DataRequired()
        ]
    )
    cwdn1 = IntegerField(
        label='Course Woody Debris - Nest 1',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    cwdn2 = IntegerField(
        label='Course Woody Debris - Nest 2',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    cwdn3 = IntegerField(
        label='Course Woody Debris - Nest 3',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    cwdlog = IntegerField(
        label='Course Woody Debris - Logs',
        default=0,
        validators=[
            NumberRange(min=0),
            InputRequired()
        ]
    )
    water_temp = DecimalField(
        label='Water Temperature'
    )
    ambient_temp = DecimalField(
        label='Ambient Temperature'
    )
    precentage_disolved_oxygen = DecimalField(
        label='% Disolved Oxygen'
    )
    salinity = DecimalField(
        label='Salinity in ppt'
    )
    specific_conductance = DecimalField(
        label='Specific Conductance'
    )
    conductivity = DecimalField(
        label='Conductivity'
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()


class survey_camera_form(FlaskForm):
    survey_id = HiddenField(
        label='survey',
        validators=[
            DataRequired()
        ]
    )
    camera = SelectField(
        label='Camera',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    card_in = SelectField(
        label='Card In',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    card_out = SelectField(
        label='Card Out',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    cleared = BooleanField(
        label='Has out SD card been cleared?',
        default=False
    )
    changed_battery = BooleanField(
        label='Changed Batteries?',
        default=False
    )
    functional = BooleanField(
        label='Is/was the camera functional?',
        default=False
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()


class survey_predator_form(FlaskForm):
    survey_id = HiddenField(
        label='survey',
        validators=[
            DataRequired()
        ]
    )
    sighting_choices = [
        ('sighting', 'Sighting'),
        ('scat', 'Scat'),
        ('track', 'Track'),
        ('chick_mort', 'Chick Mortality'),
        ('adult_mort', 'Adult Mortality'),
        ('nest_dest', 'Nest Destruction'),
    ]
    sighting_type = SelectField(
        label='Sighting Method',
        choices=sighting_choices,
        validators=[
            DataRequired()
        ]
    )
    predator_id = SelectField(
        label='Predator',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    count = IntegerField(
        label='Count',
        validators=[
            DataRequired()
        ]
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()


class survey_predator_camera_form(FlaskForm):
    survey_id = HiddenField(
        label='survey',
        validators=[
            DataRequired()
        ]
    )
    predator_id = SelectField(
        label='Predator',
        coerce=int,
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    start = DateTimeLocalField(
        label='Time In',
        format='%Y-%m-%dT%H:%M',
        validators=[
            DataRequired()
        ]
    )
    end = DateTimeLocalField(
        label='Time Out',
        format='%Y-%m-%dT%H:%M',
        validators=[
            DataRequired()
        ]
    )
    count = IntegerField(
        label='Count',
        validators=[
            DataRequired()
        ]
    )
    scat = BooleanField(
        label='Scat?'
    )
    adult_mort = BooleanField(
        label='Adult Mortality?'
    )
    chick_mort = BooleanField(
        label='Chick Mortality?'
    )
    nest_dest = BooleanField(
        label='Nest Destruction?'
    )
    comment = TextAreaField(
        label='Comments',
        default=''
    )
    submit = SubmitField()
