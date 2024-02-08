import os
from flask import request, jsonify, g
from app import app
from run_opendss import run_opendss
from generate_dss_script import generate_dss_script

@app.route('/process-data', methods=['POST'])
def process_data():
    
    # 接收 JSON 数据
    data = request.json
    g.received_data = data

    # 生成 OpenDSS 脚本文件, 生成的脚本文件放在工程路径下的opendss_script_files中
    dss_script_filename = generate_dss_script(data, os.path.join("opendss_script_files"))
    g.opendss_script_file = dss_script_filename

    # 运行 OpenDSS 计算
    result = run_opendss(dss_script_filename)
    g.result = result

    return jsonify(result)