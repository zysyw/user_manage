from flask import Blueprint
from flask_admin import Admin
from app import app
from flask_admin.contrib.peewee import ModelView

from models import User, UserRoles, Role

#admin_blueprint = Blueprint('admin', __name__)

admin = Admin(app, name='后台管理', base_template='my_master.html', template_mode='bootstrap4')

class UserAdmin(ModelView):
    # 设置列表视图格式
    column_list = ('username', 'email', 'roles')
    column_labels = dict(username='用户名称', email='电子邮件', roles='角色')
    def _list_roles(view, context, model, name):
        # 用于生成显示作者相关书籍的 HTML
        roles = (Role.select().join(UserRoles).join(User).where(User.id == model.id))
        return ', '.join([role.name for role in roles])

    column_formatters = {
        'roles': _list_roles
    }

admin.add_view(UserAdmin(User, name='用户管理'))