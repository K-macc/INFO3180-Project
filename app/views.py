"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from binascii import Error

from flask import request, jsonify, send_file, send_from_directory, make_response, session, g
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db
from app.models import User, Profile, Favourite
from app.forms import UserForm, ProfileForm, LoginForm, RegistrationForm
from flask import flash

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': r'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}), 200

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/register', methods=['POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return jsonify({"error": "Username already exists!!"}), 400
        elif User.query.filter_by(email=form.email.data).first():
            return jsonify({"error": "Email Address already exists!!"}), 400
        else:
            new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            name=form.name.data,
            email=form.email.data
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
            "message": "User registered successfully!!",
            'user' : {
                'id': new_user.id,
                'username': new_user.username,
                'name': new_user.name,
                'email': new_user.email
                }
            }), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            token=jwt.encode({
            'user_id': user.id,
            'iat': datetime.utcnow(),  # Issued at time
            'exp': datetime.utcnow() + timedelta(hours=2)  # Token expires in 1 hour
            }, app.config['SECRET_KEY'], algorithm='HS256')
            session['user_id'] = user.id  # Store user ID in session
            login_user(user)
            return jsonify({
                "message": "Logged in successfully!!",
                'token': token,
                'id': user.id,
                'user': {
                    'username': user.username,
                    'name': user.name,
                }}), 200
        else:
            return jsonify({"error": "Invalid username or password!!"}), 401
    else:
        return jsonify({"error": form_errors(form)}), 400
    

@app.route('/api/auth/logout', methods=['POST'])
@requires_auth 
def logout():
    try:
        session.pop('user_id', None)  # Remove user ID from session
        logout_user()
        return jsonify({"message": "Logged out successfully!!"}), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route('/api/profiles', methods=['GET'])
@requires_auth
def get_profiles():
    current_user_id = g.current_user['user_id']  # Get the user ID from the JWT payload
    
    # Get all profiles except the current user's
    profiles = Profile.query.filter(Profile.user_id_fk != current_user_id).all()
    
    profiles_list = []
    for profile in profiles:
        profiles_list.append({
            'id': profile.id,
            'user_id': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        })
    
    return jsonify({'profiles': profiles_list}), 200
###
# The functions below should be applicable to all Flask apps.
###
def has_complete_profile(user_id):
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    return any(p.is_complete() for p in profiles)

## Vedang's Flask Endpoints starts here - Part 1

@app.route('/api/profiles', methods=['POST'])
@requires_auth  
def create_profile():
    form = ProfileForm()
    user_id = session.get('user_id') 
    
    if form.validate_on_submit():
        if Profile.query.filter_by(user_id_fk=user_id).count() >= 3:
            return jsonify({"error": "Max 3 profiles allowed"}), 400
        else:
            profile = Profile(
                user_id_fk=user_id,
                description=form.description.data,
                parish=form.parish.data,
                biography=form.biography.data,
                sex=form.sex.data,
                race=form.race.data,
                birth_year=form.birth_year.data,
                height=form.height.data,
                fav_cuisine=form.fav_cuisine.data,
                fav_colour=form.fav_colour.data,
                fav_school_subject=form.fav_school_subject.data,
                political=form.political.data,
                religious=form.religious.data,
                family_oriented=form.family_oriented.data
            )  
            db.session.add(profile)
            db.session.commit()
            return jsonify({"message":"New Profile Created!!"}), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400

@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@requires_auth
def get_profile(profile_id):
    # Check if profile is complete for the current user 
    if not has_complete_profile(current_user.id):
        return jsonify({"error": "Complete your profile to access this feature."}), 403

    profile = Profile.query.get_or_404(profile_id)
    return jsonify({"profile":profile.serialize()}), 200

@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@requires_auth  
def add_favourite(user_id):
    
    u_id = session.get('user_id')
    
    if not has_complete_profile(u_id):
        return jsonify({"error": "Complete your profile to access this feature."}), 403
    
    if user_id == u_id:  
        return jsonify({"error": "Cannot favourite yourself"}), 400

    profile = Profile.query.filter_by(user_id_fk=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    fav = Favourite.query.filter_by(user_id_fk=u_id, fav_user_id_fk=user_id).first()
    if fav:
        return jsonify({"message": "Already added to favourites"}), 200

    fav = Favourite(user_id_fk=u_id, fav_user_id_fk=user_id)
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


@app.route('/api/search', methods=['GET'])
def search_profiles():
    try:
        name = request.args.get('name', default='', type=str)
        birth_year = request.args.get('birth_year', default=None, type=int)
        sex = request.args.get('sex', default='', type=str)
        race = request.args.get('race', default='', type=str)
        query = """
            SELECT p.id, p.user_id_fk, p.description, p.parish, p.biography, p.sex, p.race, p.birth_year, p.height, 
                   p.fav_cuisine, p.fav_colour, p.fav_school_sibject, p.political, p.religious, p.family_oriented
            FROM profile p
            JOIN users u ON p.user_id_fk = u.id
            WHERE u.name = %s
            AND p.birth_year = %s
            AND p.sex = %s
            AND p.race = %s;
        """
        params = (name, birth_year, sex, race)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if not results:
            return make_response(jsonify({"error": "No profiles matched your search"}), 404)
        return make_response(jsonify(results), 200)
    except Error as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        profiles = db.session.query(Profile).filter_by(user_id_fk=user_id).all()
        if not profiles:
            return jsonify({"error": "No profiles found for this user"}), 404
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "photo": f"/api/photo/{user.photo}",
            "date_joined": user.date_joined.strftime('%Y-%m-%d')  
        }
        
        profiles_data = [
            {
                "id": profile.id,
                "description": profile.description,
                "parish": profile.parish,
                "biography": profile.biography,
                "sex": profile.sex,
                "race": profile.race,
                "birth_year": profile.birth_year,
                "height": profile.height,
                "fav_cuisine": profile.fav_cuisine,
                "fav_colour": profile.fav_colour,
                "fav_school_subject": profile.fav_school_subject,
                "political": profile.political,
                "religious": profile.religious,
                "family_oriented": profile.family_oriented
            }
            for profile in profiles
        ]
        
        return jsonify({
            "user": user_data,
            "profiles": profiles_data
             }),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.username, u.password, u.name, u.email, u.photo, u.date_joined 
            FROM users u
            JOIN favourite f ON u.id = f.user_id_fk
            WHERE f.user_id_fk = %s
        """, (user_id,))
        favourites = cursor.fetchall()
        if not favourites:
            return make_response(jsonify({"error": "No favourites found for this user"}), 404)
        return make_response(jsonify(favourites), 200)
    except Error as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()

@app.route('/api/users/favourites/<int:N>', methods=['GET'])
def get_top_favoured_users(N):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.username, u.password, u.name, u.email, u.photo, u.date_joined, COUNT(f.user_id_fk) AS favourites_count
            FROM users u          
            JOIN favourite f ON u.id = f.user_id_fk       
            GROUP BY u.id, u.username, u.name
            ORDER BY favourites_count DESC
            LIMIT %s
        """, (N,))
        top_favourites = cursor.fetchall()
        if not top_favourites:
            return make_response(jsonify({"error": "No favoured users found"}), 404)
        return make_response(jsonify(top_favourites), 200)
    except Error as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()


@app.route('/api/photo/<filename>', methods = ['GET'])
def get_photo(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']),filename),200

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
    return jsonify({'error': 'Not found'}), 404
    # return render_template('404.html'), 404