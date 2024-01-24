from flask_admin import Admin
from app import app

admin = Admin(app, name='microblog', template_mode='bootstrap3')