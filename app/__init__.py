from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id  # should be an int or string, no 'subject' field needed


# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define the login view name

# Define the user_loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User 
    return User.query.get(int(user_id))




# Import views (this should come after initializing the app and extensions)
from app import views

