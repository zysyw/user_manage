from app import app
from flask import render_template, render_template_string
from flask_security import auth_required

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')