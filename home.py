from flask import Blueprint, render_template
from flask_security import auth_required

home = Blueprint('home', __name__)

@home.route('/home', methods=['GET'])
@auth_required()
def show():
    return render_template('home.html')
