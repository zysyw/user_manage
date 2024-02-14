from flask import Blueprint, current_app, jsonify, render_template
import json
from flask_security import current_user
from opendss_data.data_models import Calculation_Process

# 创建一个蓝图
received_data_bp = Blueprint('received_data_bp', __name__)

@received_data_bp.route('/received-data')
def receive_data():
    try:
        # 尝试获取配置数据
        user_processes = Calculation_Process.select().where(Calculation_Process.user == current_user)
        
        data = current_app.config.get('received_data')
        if data is None:
            raise KeyError("未找到配置中的'received_data'键")
        
        # 尝试将数据序列化为JSON
        data_str = json.dumps(data, ensure_ascii=False)
        data_str = user_processes.json_data
        
    except KeyError as e:
        # 如果在配置中找不到键，返回一个自定义的错误页面或JSON响应
        return jsonify({'error': str(e)}), 500
    except TypeError as e:
        # 如果数据无法序列化成JSON，返回一个自定义的错误页面或JSON响应
        return jsonify({'error': '数据序列化错误'}), 500
    else:
        # 如果一切正常，渲染模板
        return render_template('show_data.html', dict_data=data_str)

# 可选：全局错误处理器
@received_data_bp.app_errorhandler(500)
def internal_error(error):
    return "服务器内部错误", 500