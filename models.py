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
    username = TextField()
    email = TextField() # unique email
    password = TextField()
    active = BooleanField(default=True)
    fs_uniquifier = TextField(null=False)
    confirmed_at = DateTimeField(null=True) # for flask-security, not required
    
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
    expiry_date = DateField()  # 到期日期
    status = BooleanField()  # 缴费状态，已缴费为True，未缴费为False
    remarks = CharField(null=True)  # 备注，可选  
