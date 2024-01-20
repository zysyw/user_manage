from flask_security import hash_password
from app import app, db

from modles import *   
from auth import * 
from views import *

def create_tables():
    for Model in (Role, User, UserRoles):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    with app.app_context():
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8080)