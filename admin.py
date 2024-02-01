from flask_admin import Admin, AdminIndexView
from app import app
from flask_admin.contrib.peewee import ModelView
from flask_security import current_user, roles_required
from models import User, UserRoles, Role
from flask import redirect, url_for, request

class MyAdminIndexView(AdminIndexView):
    #@roles_required('administrator')  # 仅允许角色为'administrator'的用户访问
    def is_accessible(self):
        # 检查用户是否登录并且拥有 'administrator' 角色
        return current_user.is_authenticated and current_user.has_role('administrator')

    def inaccessible_callback(self, name, **kwargs):
        # 如果用户未登录，则重定向到登录页面
        if not current_user.is_authenticated:
            return redirect(url_for('security.login', next=request.url))
        # 如果用户登录但没有权限，显示一个友好的错误消息
        return "<h3>Forbidden</h3><p>You don't have the permission to access this resource.</p>", 403

admin = Admin(app, index_view=MyAdminIndexView(), name='后台管理', base_template='my_master.html', template_mode='bootstrap4')

class UserAdmin(ModelView):
    # 设置列表视图格式
    column_list = ('username', 'email', 'roles')
    column_labels = dict(username='用户名称', email='电子邮件', roles='权限')
    def _list_roles(view, context, model, name):
        # 取得用户相关的角色
        return ', '.join([role.name for role in model.roles])

    column_formatters = {
        'roles': _list_roles
    }

admin.add_view(UserAdmin(User, name='用户管理'))