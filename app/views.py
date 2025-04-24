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

from flask import render_template, request, jsonify, send_file, send_from_directory, make_response
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


from app import app, db
from app.models import User, Profile, Favourite
from app.forms import UserForm, ProfileForm

# def requires_auth(f):
#   @wraps(f)
#   def decorated(*args, **kwargs):
#     auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

#     if not auth:
#       return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

#     parts = auth.split()

#     if parts[0].lower() != 'bearer':
#       return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
#     elif len(parts) == 1:
#       return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
#     elif len(parts) > 2:
#       return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

#     token = parts[1]
#     try:
#         payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

#     except jwt.ExpiredSignatureError:
#         return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
#     except jwt.DecodeError:
#         return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

#     g.current_user = user = payload
#     return f(*args, **kwargs)

#   return decorated

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ['username', 'password', 'name', 'email']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    try:
        new_user = User(
            
            username=data['username'],
            password=generate_password_hash(data['password']),  # Secure the password
            name=data['name'],
            email=data['email'],
            date_joined=datetime.utcnow()  # Add date_joined field
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "User registered successfully",
            'user' : {
                'id': new_user.id,
                'username': new_user.username,
                'name': new_user.name,
                'email': new_user.email,
                'date_joined': new_user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                }
            }), 201

    except Exception as e:
        return jsonify({"error":"An error occurred while processing the form", "details":str(e)}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data=request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400
    
    user=User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
    
    token=jwt.encode({
        'user_id': user.id,
        'iat': datetime.utcnow(),  # Issued at time
        'exp': datetime.utcnow() + timedelta(hours=2)  # Token expires in 1 hour
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'username': user.username,
            'name': user.name,
        }
    }),200

@app.route('/api/auth/logout', methods=['POST'])
# @requires_auth 
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


@app.route('/api/profiles', methods=['GET'])
# @requires_auth
def get_profiles():
    # current_user_id = get_jwt_identity()
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
            return make_response(jsonify({"error": "User not found"}), 404)
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "photo": f"/api/photo/{user.photo}",
            "date_joined": user.date_joined.strftime('%Y-%m-%d')  # or whatever format you want
        }
        
        return make_response(jsonify(user_data), 200)
    except Exception as e:
        print(f"Error fetching user: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


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