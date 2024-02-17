from flask import render_template
from app import app

from admin.models import *   
from admin.auth import * 
from admin.admin import *
from admin.payment import *
from views import *

from opendss_calculation.calculate import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)