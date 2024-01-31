from flask import render_template
from flask_security import hash_password
from app import app, db

from models import *   
from auth import * 
#from views import *
from admin import *
from payment import *

@app.route('/')
def index():
    return render_template('index.html')

def create_tables():
    import string
    import random
    
    for Model in (Role, User, UserRoles, Payment):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    with app.app_context():
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(username='test', email="test@me.com", password=hash_password("password"))
            
    with app.app_context():    

        # 使用user_datastore.create_role创建user和administrator角色
        user_role = user_datastore.create_role(name='user')
        administrator_role = user_datastore.create_role(name='administrator')

        # 设置管理员测试账号
        user_datastore.create_user(
            username='Admin',
            email='admin@example.com',
            password=hash_password('admin'),
            roles=[user_role, administrator_role]
        )

        # 设置用户测试账号
        user_datastore.create_user(
            username='SunMIn',
            email='zysyw@163.com',
            password=hash_password('123456789'),
            roles=[user_role, ]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        # 设置用户账号
        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            print(f"{tmp_email}:{tmp_pass}")
            user_datastore.create_user(
                username=first_names[i] + " " + last_names[i],
                email=tmp_email,
                password=hash_password(tmp_pass),
                roles=[user_role, ]
            )
            
        print(send_mail())

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8080)