from flask_admin.contrib.peewee import ModelView
from .data_modles import *
from admin.admin import admin
from flask_security import current_user

class UserCalculationProcessView(ModelView):
    column_list = ('upload_time', 'short_json_data', 'short_opendss_script')
    column_labels = dict(upload_time='上传日期', short_json_data='上传数据', short_opendss_script='opendss脚本')
    can_create = False
    can_delete = False
    can_edit = False

    def get_query(self):
        return super(UserCalculationProcessView, self).get_query().where(Calculation_Process.user == current_user)

    def get_count_query(self):
        return super(UserCalculationProcessView, self).get_count_query().where(Calculation_Process.user == current_user)
    
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return any(role.name == 'user' for role in current_user.roles)

    # 将格式化函数应用到json_data字段和opendss_script字段
    column_formatters = {
        'short_json_data': lambda v, c, m, p: m.json_data[:50] + '...' if m.json_data and len(m.json_data) > 50 else m.json_data,
        'short_opendss_script': lambda v, c, m, p: m.opendss_script[:50] + '...' if m.opendss_script and len(m.opendss_script) > 50 else m.opendss_script
    }
    
admin.add_view(UserCalculationProcessView(Calculation_Process, name='计算记录', endpoint='user_calculation'))