import json
from app import app
from flask import Blueprint, request, jsonify, current_app
from .run_opendss import run_opendss
from .generate_dss_script import generate_dss_script
from flask_security import auth_token_required, current_user
from opendss_data.data_modles import *
from admin.models import User

@app.route('/api/process-data', methods=['POST'])
@auth_token_required
def process_data():
    current_user_db = User.get(User.username == current_user.username)
    new_process = Calculation_Process.create(
        user = current_user_db
    )
    clean_up_all_results(new_process.user)

    # 接收 JSON 数据
    data = request.json
    new_process.json_data = json.dumps(data, ensure_ascii=False)

    # 生成 OpenDSS 脚本文件, 生成的脚本文件放在opendss_script_files中
    dss_script = generate_dss_script(data)
    new_process.opendss_script = dss_script
    new_process.save()

    # 运行 OpenDSS 计算 
    result = run_opendss(dss_script, new_process)
    new_process.save()

    return jsonify(result)

def clean_up_all_results(user):
    # 获取用户的所有 Calculation_Process 记录
    processes = Calculation_Process.select().where(Calculation_Process.user == user)
    
    # 遍历所有 Calculation_Process 记录
    for process in processes:
        VI.delete().where(VI.calculation_process == process).execute()
        VIHourValue.delete().where(VIHourValue.vi == VI.select().where(VI.calculation_process == process)).execute()
        Loss.delete().where(Loss.calculation_process == process).execute()
