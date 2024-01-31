import os
from datetime import timedelta

# Flask Configurations for ENVT

# Statement for enabling the development environment
    # Convert to False in production.
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask Secret Key. 
SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

# Define the database - we are working with PeeWee
PEEWEE_DATABASE_URI = os.path.join(BASE_DIR, os.environ.get('PEEWEE_DATABASE_URI'))
DATABASE = {
    'name': PEEWEE_DATABASE_URI,
    'engine': 'peewee.SqliteDatabase',
}

# Enable protection agains *Cross-site Request Forgery (CSRF)*
#CSRF_ENABLED = True
# Use a secure, unique and absolutely secret key for
# signing the data. 
#CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')

# Session Cache time
#PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.environ.get("PERMANENT_SESSION_LIFETIME")))

#Flask Security Log in 
SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_SALT = "some_long_random_text"
SECURITY_PASSWORD_HASH = "pbkdf2_sha256" # use "pbkdf2_sha256" on Windows machines. 
#SECURITY_TRACKABLE = True

# Defining the type of passwords to be set by user at register. 
#SECURITY_PASSWORD_LENGTH_MIN = 6
#SECURITY_PASSWORD_COMPLEXITY_CHECKER = None # Set to True on Production. 
#SECURITY_FRESHNESS_GRACE_PERIOD = timedelta(minutes=15)

## Flask Security email Config (# Remove the parameter once in prod)
SECURITY_SEND_REGISTER_EMAIL = True
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("Mail_Username")
MAIL_PASSWORD = os.environ.get("Mail_Password")

## Localization
BABEL_DEFAULT_LOCALE = 'zh_CN'

## Flask-Admin settings
FLASK_ADMIN_SWATCH = 'cerulean'