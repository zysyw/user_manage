from flask_admin import Admin, AdminIndexView
from app import app
from flask_admin.contrib.peewee import ModelView
from flask_security import current_user, roles_required
from models import User, UserRoles, Role
from flask import redirect, url_for, request

class IndexView(AdminIndexView): # 程序主页面允许游客访问、登录和注册，所以不需要权限
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # 如果用户未登录，则重定向到登录页面
        if not current_user.is_authenticated:
            return redirect(url_for('security.login', next=request.url))
        # 如果用户已登录，则进入“Home”页面
        return redirect(url_for('forbidden'))

index_view = AdminIndexView(endpoint='powerloss', url='/powerloss') # 程序主页面
admin = Admin(app, index_view=index_view, name='后台管理', endpoint='powerloss', url='/powerloss', base_template='my_master.html', template_mode='bootstrap4')

class UserAdmin(ModelView): # 用户的管理页面
    # 设置列表视图格式
    column_list = ('username', 'email', 'roles')
    column_labels = dict(username='用户名称', email='电子邮件', roles='权限')
    
    def _list_roles(view, context, model, name):
        # 取得用户相关的角色
        return ', '.join([role.name for role in model.roles])

    column_formatters = {
        'roles': _list_roles
    }
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return any(role.name == 'administrator' for role in current_user.roles)

admin.add_view(UserAdmin(User, name='用户管理'))