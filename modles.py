from app import app, db
from peewee import *
from flask_security import UserMixin, RoleMixin

class Role(RoleMixin, db.Model):
    name = CharField(unique=True)
    description = TextField(null=True)
    permissions = TextField(null=True)

# N.B. order is important since db.Model also contains a get_id() -
# we need the one from UserMixin.
class User(UserMixin, db.Model):
    email = TextField() # unique email
    password = TextField()
    active = BooleanField(default=True)
    fs_uniquifier = TextField(null=False)
    confirmed_at = DateTimeField(null=True) # for flask-security, not required

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
