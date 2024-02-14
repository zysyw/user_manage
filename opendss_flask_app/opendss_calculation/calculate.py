import json
import os
from flask import Blueprint, request, jsonify, current_app
from .run_opendss import run_opendss
from .generate_dss_script import generate_dss_script
from flask_security import auth_token_required, current_user
from opendss_data.data_models import Calculation_Process
from admin.models import User

calculate_bp = Blueprint('calculate', __name__)

@calculate_bp.route('/api/process-data', methods=['POST'])
@auth_token_required
def process_data():
    current_user_db = User.get(User.username == current_user.username)
    new_process = Calculation_Process.create(
        user = current_user_db
    )

    # 接收 JSON 数据
    data = request.json
    new_process.json_data = json.dumps(data)
    current_app.config['received_data'] = data

    # 生成 OpenDSS 脚本文件, 生成的脚本文件放在opendss_script_files中
    dss_script_filename = generate_dss_script(data, os.path.join(os.path.dirname(os.path.abspath(__file__)), "opendss_script_files"))
    print("Generated DSS script file:", dss_script_filename)
    current_app.config['opendss_script_file'] = dss_script_filename

    # 运行 OpenDSS 计算
    result = run_opendss(dss_script_filename)
    current_app.config['result'] = result

    return jsonify(result)