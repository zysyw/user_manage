from flask_admin.contrib.peewee import ModelView
from .data_modles import *
from admin.admin import admin
from flask_security import current_user
from markupsafe import Markup

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
    
    def _format_short_json_data(v, c, m, p):
        short_display = m.json_data[:50] + '...' if m.json_data and len(m.json_data) > 50 else m.json_data
        # 创建链接
        link = Markup(f'<a href="/received-data/{m.id}">{short_display}</a>')
        return link
    
    def _format_short_opendss_script(v, c, m, p):
        short_display = m.opendss_script[:50] + '...' if m.opendss_script and len(m.opendss_script) > 50 else m.opendss_script
        # 创建链接
        link = Markup(f'<a href="/opendss-script/{m.id}">{short_display}</a>')
        return link

    # 将格式化函数应用到json_data字段和opendss_script字段
    column_formatters = {
        'short_json_data': _format_short_json_data,
        'short_opendss_script': _format_short_opendss_script
    }

class VIView(ModelView):
    column_list = ('component_name', 'unit', 'hourly_values')
    column_labels = dict(component_name='组件名称', unit='单位', hourly_values='整点数据')
    can_create = False
    can_delete = False
    can_edit = False
    column_sortable_list = ('component_name',)

    def get_query(self):
        return super(VIView, self).get_query().join(Calculation_Process).where(Calculation_Process.user == current_user)

    def get_count_query(self):
        return super(VIView, self).get_count_query().join(Calculation_Process).where(Calculation_Process.user == current_user)
    
    def _format_hourly_values(v, c, m, p):
        hourly_values_display = ', '.join(m.generate_hourly_values())
        return hourly_values_display
    
    column_formatters = {
        'hourly_values': _format_hourly_values
    }
    
class LossView(ModelView):
    column_list = ('component_name', 'unit', 'total_loss', 'load_loss', 'no_load_loss')
    column_labels = dict(component_name='组件名称', unit='单位', total_loss='总损耗', load_loss='负载损耗', no_load_loss='空载损耗')
    can_create = False
    can_delete = False
    can_edit = False

    def get_query(self):
        return super(LossView, self).get_query().join(Calculation_Process).where(Calculation_Process.user == current_user)

    def get_count_query(self):
        return super(LossView, self).get_count_query().join(Calculation_Process).where(Calculation_Process.user == current_user)
    
    def _format_value(v, c, m, p):
        # 获取指定列的值
        value = getattr(m, p)
        # 返回格式化后的字符串，保留两位小数
        return '{:.2f}'.format(value)

    column_formatters = {
        'total_loss': _format_value,
        'load_loss': _format_value,
        'no_load_loss': _format_value
    }

admin.add_view(UserCalculationProcessView(Calculation_Process, name='计算记录', endpoint='user_calculation'))
admin.add_view(VIView(VI, name='VI', endpoint='calculation_VI'))
admin.add_view(LossView(Loss, name='损耗', endpoint='calculation_Loss'))