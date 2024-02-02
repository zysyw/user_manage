from app import app
from flask import render_template, render_template_string
from flask_security import auth_required

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    # add a user
    
    return render_template_string("""
        <form action="{{ url_for_security('register') }}" method="POST" name="register">
            {{ register_user_form.hidden_tag() }}
            {{ register_user_form.email }}
            {{ register_user_form.password }}
            {{ register_user_form.password_confirm }}
            {{ register_user_form.submit }}
        </form>
    """)

@app.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')