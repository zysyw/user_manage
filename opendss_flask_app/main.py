from flask import render_template
from app import app

from admin.models import *   
from admin.auth import * 
from admin.admin import *
from admin.payment import *
from admin.views import *

from opendss_calculation.calculate import calculate_bp
from opendss_calculation.received_data import received_data_bp
from opendss_calculation.generate_dss_script import opendss_script_bp
from opendss_calculation.run_opendss import run_opendss_bp

app.register_blueprint(calculate_bp)
# 显示json数据、opendss脚本文件、opendss计算结果的蓝图
app.register_blueprint(received_data_bp)
app.register_blueprint(opendss_script_bp)
app.register_blueprint(run_opendss_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)