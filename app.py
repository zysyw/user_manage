import os
from flask import Flask
from playhouse.flask_utils import FlaskDB
from dotenv import load_dotenv
from flask_babel import Babel
from flask_apscheduler import APScheduler

# VARIABLE PARAMETERS
load_dotenv('.env')

# Create app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')

# Create database connection object
db = FlaskDB(app)

# Localization
babel = Babel(app)

# 启用定时更新缴费状态和通知用户的功能
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()