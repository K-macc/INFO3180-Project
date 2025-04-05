# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, BooleanField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    photo = FileField('User Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'images only!')])


class ProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired()])
    parish = StringField('Parish', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    sex = SelectField('Sex', choices = [ ('male', 'Male'), ('female', 'Female') ], validators=[InputRequired()])
    race = SelectField('Race', choices = [ ('black', 'Black'), ('white', 'White'), ('asian', 'Asian'), ('indigenous', 'Indigenous'), ('mixed','Mixed') ], validators=[InputRequired()])
    birth_year = IntegerField('Birth Year', validators=[InputRequired(), NumberRange(min=1900, max=2025, message="Enter a valid year")])
    height = FloatField("Height", validators=[InputRequired(), NumberRange(min=50, max=300, message="Enter your height in cm")])
    fav_cuisine = StringField('Favorite Cuisine', validators=[InputRequired()])
    fav_colour = StringField('Favorite Colour', validators=[InputRequired()])
    fav_school_subject = StringField('Favorite School Subject', validators=[InputRequired()])
    political = BooleanField('Political')
    religious = BooleanField('Religious')
    family_oriented = BooleanField('Family Oriented')
    

