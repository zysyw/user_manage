from app import app, db
from flask_security import Security, PeeweeUserDatastore
from modles import *

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
app.security = Security(app, user_datastore) 