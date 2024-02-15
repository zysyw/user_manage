from flask import Blueprint, current_app, jsonify, render_template
import json
from flask_security import current_user
from opendss_data.data_modles import Calculation_Process

# 创建一个蓝图
received_data_bp = Blueprint('received_data_bp', __name__)

@received_data_bp.route('/received-data')
def receive_data():
    try:
        # 尝试获取当前用户最后一个上传时间的Calculation_Process
        last_uploaded_process = (Calculation_Process
                                 .select()
                                 .where(Calculation_Process.user == current_user)
                                 .order_by(Calculation_Process.upload_time.desc())
                                 .get())
        
        return render_template('show_data.html', dict_data = last_uploaded_process.json_data)

    except Calculation_Process.DoesNotExist:
        # 如果未找到任何记录，返回错误消息
        return render_template('show_data.html', dict_data = jsonify({"message": "未找到计算记录"}))