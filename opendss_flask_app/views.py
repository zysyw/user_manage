from app import app
from flask import jsonify, render_template, render_template_string, request
from flask_security import auth_required, auth_token_required, login_user, current_user, verify_password
from admin.models import User
from opendss_data.calculation_data_views import *

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/received-data/<int:id>')
def receive_data(id):
    try:
        process = Calculation_Process.get_by_id(id)
        if process.user == current_user:        
            return render_template('show_data.html', content = process.json_data)
        else:
            # 如果找到的记录不属于当前用户，返回错误消息
            return jsonify({"message": "未找到计算记录"}), 404

    except Calculation_Process.DoesNotExist:
        # 如果未找到任何记录，返回错误消息
        return render_template('show_data.html', content = jsonify({"message": "未找到计算记录"}))

@app.route('/opendss-script/<int:id>')
def show_opendss_script(id):
    try:
        process = Calculation_Process.get_by_id(id)
        if process.user == current_user:
            content = process.opendss_script
            return render_template('show_script.html', content = content.split('\n'))
        else:
            # 如果找到的记录不属于当前用户，返回错误消息
            return jsonify({"message": "未找到计算记录"}), 404

    except Calculation_Process.DoesNotExist:
        # 如果未找到任何记录，返回错误消息
        return render_template('show_script.html', dict_data = jsonify({"message": "未找到计算记录"}))# 从配置中获取文件名

# 以下程序实际上是不需要的，因为flask-security-too有自己的/login端点，它既可以以浏览器发起登录请求，也可以以json发起请求
# 下面这个程序比较简单，不如原生程序功能完整
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    user = User.get(User.username == username)
    with app.app_context():
        password = request.json.get('password')
        if user and verify_password(password, user.password):
            login_user(user)
            token = current_user.get_auth_token()
            return jsonify({'auth_token': token})
        return jsonify({'message': '用户名或密码错误'}), 401
    
@app.route('/api/test-token', methods=['POST'])
@auth_token_required
def test():
    return jsonify({'message': 'You are authenticated'})

@app.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')