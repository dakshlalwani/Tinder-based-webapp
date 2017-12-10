# Import flask and template operators
from flask import Flask, render_template, session, jsonify

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps
from flask_login import LoginManager,UserMixin

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
   return render_template('homepage.html'), 200

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'http://127.0.0.1:5000/login'

# Import a module / component using its blueprint handler variable (mod_auth)
from app.user.controllers import mod_user
from app.like.controllers import mod_like
from app.match.controllers import mod_match

# Register blueprint(s)
app.register_blueprint(mod_user)
app.register_blueprint(mod_like)
app.register_blueprint(mod_match)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()