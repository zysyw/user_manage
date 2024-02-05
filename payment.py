# payment.py
from flask import Blueprint, request, jsonify
from models import Payment, User  
from datetime import datetime, timedelta
from flask_admin.contrib.peewee import ModelView
from admin import admin
from flask_security import current_user

payment_blueprint = Blueprint('payment', __name__)

class PaymentAdmin(ModelView):
    # 设置payment类的列表视图格式
    column_list = ('user', 'payment_date', 'amount', 'validity_period', 'expiry_date', 'status', 'remarks')
    # 设置编辑和创建表单中显示的字段
    form_columns = ('user', 'payment_date', 'amount', 'validity_period', 'remarks')
    
    column_labels = dict(user='用户', payment_date='缴费日期', amount='缴费金额', validity_period='有效期限', expiry_date='到期日期', status='缴费状态', remarks='备注')
    column_filters = (User.username, )    

    form_ajax_refs = {
        'user': {
            'fields': (User.username, 'email')
        }
    }

    def on_model_change(self, form, model, is_created):
        """
        这个方法会在模型被修改之后、写入数据库之前调用
        """
        if is_created:
            # 设置到期日期
            last_payment = Payment.select().where(Payment.user == model.user).order_by(Payment.expiry_date.desc()).first()
            if last_payment and last_payment.expiry_date > datetime.now().date():
                model.expiry_date = last_payment.expiry_date + timedelta(days=model.validity_period)
            else:
                model.expiry_date = model.payment_date + timedelta(days=model.validity_period)

        super(PaymentAdmin, self).on_model_change(form, model, is_created)

# 使用flask-admin的baseView创建单个用户缴费记录的视图，用户只能浏览自己的缴费记录，不能增加、删除和修改
# 如果用户无相关的缴费记录，则显示“无缴费记录”
class UserPaymentView(ModelView):
    column_list = ('payment_date', 'amount', 'validity_period', 'expiry_date', 'status', 'remarks')
    column_labels = dict(payment_date='缴费日期', amount='缴费金额', validity_period='有效期限', expiry_date='到期日期', status='缴费状态', remarks='备注')
    can_create = False
    can_delete = False
    can_edit = False
    column_filters = (Payment.payment_date, )

    def get_query(self):
        return super(UserPaymentView, self).get_query().where(Payment.user == current_user)

    def get_count_query(self):
        return super(UserPaymentView, self).get_count_query().where(Payment.user == current_user)

admin.add_view(PaymentAdmin(Payment, name='缴费管理'))

def update_payment_records():
    # 按当天日期更新缴费记录

    today = datetime.now().date()

     # 查询所有尚未过期的缴费记录
    active_payments = Payment.select().where(Payment.status != '过期')

    for payment in active_payments:
        # 计算缴费记录的到期日期
        expiry_date = payment.payment_date + timedelta(days=payment.validity_period)

        # 检查是否过期
        if expiry_date < today:
            # 标记为过期
            payment.status = '过期'
            payment.save()

def check_and_notify():
    # 检查并通知用户的逻辑
    # ...
    pass