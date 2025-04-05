# Add any model classes for Flask-SQLAlchemy here
from app import db

class User(db.Model):
    """User model for the application"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(120), nullable=True)  # Path to the photo file
    date_joined = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'
    

class Profile(db.Model):
    """Profile model for the application"""
    __tablename__ = 'profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    parish = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    race = db.Column(db.String(10), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(80), nullable=False)
    fav_colour = db.Column(db.String(80), nullable=False)
    fav_school_subject = db.Column(db.String(80), nullable=False)
    political = db.Column(db.Boolean, nullable=False, default=False)
    religious = db.Column(db.Boolean, nullable=False, default=False)
    family_oriented = db.Column(db.Boolean, nullable=False, default=False)
    
    
    def __repr__(self):
        return f'<Profile {self.user_id}>'
    

class Favourite(db.Model):
    """Favorite model for the application"""
    __tablename__ = 'favourite'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Favourite {self.user_id}>'
    
    