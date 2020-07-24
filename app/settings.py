# Settings common to all environments (development|staging|production)

# Application settings
APP_NAME = "ATU Interior Least Tern Data Colletion"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_TIME_LIMIT = 86400
