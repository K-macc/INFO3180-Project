# Add any model classes for Flask-SQLAlchemy here
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

year = datetime.now().year

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(120), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    profiles = db.relationship('Profile', backref='user', lazy=True)
    favourites = db.relationship('Favourite', backref='user', lazy=True)

     # Add the required methods for Flask-Login
    def is_active(self):
        # Return whether the user is active; return True for now
        return True

    def is_authenticated(self):
        # Flask-Login uses this to check if the user is authenticated
        return True

    def is_anonymous(self):
        # Return False to indicate that this user is not anonymous
        return False

    def get_id(self):
        # This is used to retrieve the user ID (usually the primary key)
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "photo": self.photo,
            "date_joined": str(self.date_joined)
        }


class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    parish = db.Column(db.String(80), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    race = db.Column(db.String(10), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    fav_cuisine = db.Column(db.String(80), nullable=True)
    fav_colour = db.Column(db.String(80), nullable=True)
    fav_school_subject = db.Column(db.String(80), nullable=True)
    political = db.Column(db.Boolean, nullable=True, default=False)
    religious = db.Column(db.Boolean, nullable=True, default=False)
    family_oriented = db.Column(db.Boolean, nullable=True, default=False)
    

    favourites = db.relationship('Favourite', backref='profile', lazy=True)

    def __repr__(self):
        return f'<Profile {self.id}>'
    
    def get_id(self):
        # This is used to retrieve the user ID (usually the primary key)
        return str(self.id)

    def is_complete(self):
        # Check all fields are filled (optional: make this stricter)
        return all([
            self.description, self.parish, self.biography, self.sex, self.race,
            self.birth_year, self.height, self.fav_cuisine, self.fav_colour,
            self.fav_school_subject, self.political is not None, self.religious is not None, self.family_oriented is not None
        ])

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id_fk,
            "user_name": self.user.name,
            "description": self.description,
            "parish": self.parish,
            "biography": self.biography,
            "sex": self.sex,
            "race": self.race,
            "birth_year": self.birth_year,
            "height": self.height,
            "fav_cuisine": self.fav_cuisine,
            "fav_colour": self.fav_colour,
            "fav_school_subject": self.fav_school_subject,
            "political": self.political,
            "religious": self.religious,
            "family_oriented": self.family_oriented
        }


class Favourite(db.Model):
    __tablename__ = 'favourites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)

    def __repr__(self):
        return f'<Favourite {self.user_id_fk} -> {self.fav_user_id_fk}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id_fk,
            "fav_profile_id": self.fav_user_id_fk,
            "user_name": self.profile.user.name,
            "parish": self.profile.parish,
            "age": (year - self.profile.birth_year)
        }
