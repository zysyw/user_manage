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
SECURITY_USERNAME_ENABLE = True
SECURITY_USERNAME_REQUIRED = True

# Flask-Security config
SECURITY_PASSWORD_SALT = "some_long_random_text"
SECURITY_PASSWORD_HASH = "pbkdf2_sha256" # use "pbkdf2_sha256" on Windows machines. 
#SECURITY_TRACKABLE = True

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_URL_PREFIX = "/powerloss"
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/powerloss/"
SECURITY_POST_LOGOUT_VIEW = "/powerloss/"
SECURITY_POST_REGISTER_VIEW = "/powerloss/"

# Defining the type of passwords to be set by user at register. 
#SECURITY_PASSWORD_LENGTH_MIN = 6
#SECURITY_PASSWORD_COMPLEXITY_CHECKER = None # Set to True on Production. 
#SECURITY_FRESHNESS_GRACE_PERIOD = timedelta(minutes=15)

## Flask Security email Config (# Remove the parameter once in prod)
SECURITY_CONFIRMABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_EMAIL_SENDER = 'zysyw@163.com'

## Localization
BABEL_DEFAULT_LOCALE = 'zh_CN'

## Flask-Admin settings
FLASK_ADMIN_SWATCH = 'cerulean'

## Mail settings
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_TLS =  False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = 'zysyw@163.com'

JOBS = [
        {
            'id': 'update_payment_records',
            'func': 'payment:update_payment_records',
            'trigger': 'cron',
            'hour': 9,
            'minute': 2
        },
        {
            'id': 'check_and_notify',
            'func': 'payment:check_and_notify',
            'trigger': 'cron',
            'hour': 9,
            'minute': 2
        }
    ]