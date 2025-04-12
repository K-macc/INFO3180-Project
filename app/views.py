"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask_jwt_extended import current_user
from app import app, db
from app.models import User, Profile, Favourite
from app.forms import UserForm, ProfileForm
from flask_wtf.csrf import generate_csrf
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
def has_complete_profile(user_id):
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    return any(p.is_complete() for p in profiles)

# just for testing 
@app.route('/login')
def login():
    return "Login page"

## Vedang's Flask Endpoints starts here - Part 1

@app.route('/api/profiles', methods=['POST'])
@login_required  # Uncomment to require login
def create_profile():
    data = request.json
    user_id = current_user.id  # Replace hardcoded user ID with current_user.id
    if Profile.query.filter_by(user_id_fk=user_id).count() >= 3:
        return jsonify({"error": "Max 3 profiles allowed"}), 400

    # Validate required fields
    required_fields = ['name', 'birth_year', 'sex', 'race']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "All profile fields required"}), 400

    profile = Profile(user_id_fk=user_id, **data)  # Ensuring user_id_fk is set to current_user.id
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.serialize()), 201

@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
# @login_required
def get_profile(profile_id):
    # Check if profile is complete for the current user 
    if not has_complete_profile(current_user.id):
        return jsonify({"error": "Complete your profile to access this feature."}), 403

    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.serialize())

@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@login_required  # Uncomment to require login
def add_favourite(user_id):
     # Check if profile is complete for the current user 
    if not has_complete_profile(current_user.id):
        return jsonify({"error": "Complete your profile to access this feature."}), 403
    
    if user_id == current_user.id:  # Replace hardcoded user ID with current_user.id
        return jsonify({"error": "Cannot favourite yourself"}), 400

    profile = Profile.query.filter_by(user_id_fk=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    fav = Favourite.query.filter_by(user_id=current_user.id, favourite_id=user_id).first()
    if fav:
        return jsonify({"message": "Already favourited"}), 200

    fav = Favourite(user_id=current_user.id, favourite_id=user_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Added to favourites"}), 201

@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_matches(profile_id):
    # Check if profile is complete for the current user 
    if not has_complete_profile(current_user.id):
        return jsonify({"error": "Complete your profile to access this feature."}), 403

    profile = Profile.query.get_or_404(profile_id)
    
    # Ensure the profile belongs to the current user
    if profile.user_id_fk != current_user.id:  # Use user_id_fk to compare with current_user.id
        return jsonify({"error": "Unauthorized"}), 403

    matches = Profile.query.filter(
        Profile.id != profile.id,
        Profile.user_id_fk != current_user.id,  # Use user_id_fk to filter
        Profile.birth_year == profile.birth_year,
        Profile.race == profile.race,
        Profile.sex == profile.sex,
        Profile.parish == profile.parish,
        Profile.biography == profile.biography,
        Profile.fav_cuisine == profile.fav_cuisine,
        Profile.fav_colour == profile.fav_colour,
        Profile.fav_school_subject == profile.fav_school_subject,
        Profile.political == profile.political,
        Profile.religious == profile.religious,
        Profile.family_oriented == profile.family_oriented
    ).all()

    return jsonify([p.serialize() for p in matches])

## Vedang's Flask Endpoints ends here- Part 1


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404