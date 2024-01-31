from app import app, db
from flask_security import Security, PeeweeUserDatastore
from models import *
from admin import admin
from flask_admin import helpers as admin_helpers
from flask import url_for
from flask_mailman import Mail, EmailMessage

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore) 
app.security = security

mail = Mail(app)
print("Mail Server:", app.config['MAIL_SERVER'])
print("Mail Port:", app.config['MAIL_PORT'])
print("Use TLS:", app.config['MAIL_USE_TLS'])
print("Use SSL:", app.config['MAIL_USE_SSL'])
print("Mail Username:", app.config['MAIL_USERNAME'])

msg = EmailMessage(
    'Hello',
    'Body goes here',
    'zysyw@163.com',
    ['to1@example.com', 'to2@example.com'],
    ['bcc@example.com'],
    reply_to=['another@example.com'],
    headers={'Message-ID': 'foo'},
)
with app.app_context():
    msg.send()

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )