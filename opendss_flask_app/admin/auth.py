from app import app, db
from flask_security import Security, PeeweeUserDatastore
from .models import *
from .admin import admin
from flask_admin import helpers as admin_helpers
from flask import url_for

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore) 
app.security = security

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