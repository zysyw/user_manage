from flask import Blueprint
from flask_admin import Admin
from app import app
from flask_admin.contrib.peewee import ModelView

from models import User

#admin_blueprint = Blueprint('admin', __name__)

admin = Admin(app, name='后台管理', base_template='my_master.html', template_mode='bootstrap4')

class UserAdmin(ModelView):
    pass

admin.add_view(UserAdmin(User, name='用户管理'))