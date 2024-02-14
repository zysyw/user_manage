from datetime import datetime, timedelta
from app import app, db
from peewee import *
from flask_security import UserMixin, RoleMixin

class Role(RoleMixin, db.Model):
    name = CharField(unique=True)
    description = TextField(null=True)
    permissions = TextField(null=True)
    
    def __str__(self):
        return self.name

# N.B. order is important since db.Model also contains a get_id() -
# we need the one from UserMixin.
class User(UserMixin, db.Model):
    username = TextField(unique=True)
    email = TextField(unique=True) # unique email
    password = TextField()
    active = BooleanField(default=True)
    fs_uniquifier = TextField(null=False)
    confirmed_at = DateTimeField(null=True) # for flask-security, not required
    @property
    def roles(self):
        return (Role.select().join(UserRoles).join(User).where(User.id == self.id))

    
    def __str__(self):
        return self.username

class UserRoles(db.Model):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

    def get_permissions(self):
        return self.role.get_permissions()

class Payment(db.Model):
    user = ForeignKeyField(User, backref='payments')
    payment_date = DateField() # 缴费日期
    amount = FloatField() # 缴费金额
    validity_period = IntegerField()  # 有效期限（天）
    expiry_date = DateField(null=True)
    status = CharField(null=True)
    remarks = CharField(null=True)  # 备注，可选

    def save(self, *args, **kwargs):
        
        # 查找用户当前的最后一个缴费记录
        last_payment = Payment.select().where(Payment.user == self, Payment.expiry_date >= datetime.now().date()).order_by(Payment.expiry_date.desc()).first()
        if last_payment:
            # 如果有当前的缴费记录，则在最后一个到期日的基础上增加有效期限
            self.expiry_date = last_payment.expiry_date + timedelta(days=self.validity_period)
        else:
            # 如果没有当前的缴费记录，则到期日为缴费日加上有效期限
            self.expiry_date = self.payment_date + timedelta(days=self.validity_period)
        
        today = datetime.now().date()
        self.status = "当期" if today <= self.expiry_date else "过期"
        super().save(*args, **kwargs)
