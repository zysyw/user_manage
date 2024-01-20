from app import app
from flask import render_template_string
from flask_security import auth_required

# Views
@app.route('/')
@auth_required()
def home():
    return render_template_string("Hello {{ current_user.email }}")

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