# payment.py
from flask import Blueprint, request, jsonify
from models import Payment, User  
from datetime import datetime, timedelta
from peewee import DoesNotExist
from flask_admin.contrib.peewee import ModelView
from admin import admin

payment_blueprint = Blueprint('payment', __name__)

class PaymentModelView(ModelView):
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

        super(PaymentModelView, self).on_model_change(form, model, is_created)

admin.add_view(PaymentModelView(Payment, name='缴费管理'))

def add_payment_record(user, payment_date, amount, validity_period, remarks=''):
    # 转换为日期对象，如果 payment_date 是字符串
    payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

    # 查找用户当前的最后一个缴费记录
    last_payment = Payment.select().where(Payment.user == user, Payment.expiry_date >= datetime.now().date()).order_by(Payment.expiry_date.desc()).first()

    if last_payment:
        # 如果有当前的缴费记录，则在最后一个到期日的基础上增加有效期限
        new_expiry_date = last_payment.expiry_date + datetime.timedelta(days=validity_period)
    else:
        # 如果没有当前的缴费记录，则到期日为缴费日加上有效期限
        new_expiry_date = payment_date + datetime.timedelta(days=validity_period)

    # 创建新的缴费记录
    new_payment = Payment.create(
        user=user,
        payment_date=payment_date,
        amount=amount,
        validity_period=validity_period,
        expiration_date=new_expiry_date,
        status='已缴费',
        remarks=remarks
    )
    return new_payment

def update_payment_records():
    # 每天更新缴费记录的逻辑

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