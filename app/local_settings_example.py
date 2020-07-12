import os

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# Folders for uploading and supporting documents
# THESE FOLDER MUST EXIST ON THE FILE SYSTEM
SIGNATURE_FOLDER = '/data/signatures'
SUBMISSION_FOLDER = '/data/submissions'
DOCUMENTS_FOLDER = '/data/documents'

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"
SECRET_KEY = 'This is an UNSECURE Secret. CHANGE THIS for production environments.'

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:port/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a SQLAlchemy Warning