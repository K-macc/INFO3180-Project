"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from datetime import datetime, timedelta
from binascii import Error

from flask import request, jsonify, send_from_directory, session
from flask_jwt_extended import current_user
from flask_login import login_user, logout_user
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, desc


from app import app, db
from app.models import User, Profile, Favourite
from app.forms import UserForm, ProfileForm, LoginForm
import json


def check_fields(fields):
    for key, value in fields.items():
        if value == "":
            return False
        else:
            return True


def query_profile(user_id, field):
    if len(field) == 1:
        if "sex" in field:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id, (Profile.sex == field["sex"])
            ).all()
        elif "birth_year" in field:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id,
                (
                    Profile.birth_year == int(field["birth_year"])
                    if field["birth_year"].isdigit()
                    else False
                ),
            ).all()
        else:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id, (Profile.race == field["race"])
            ).all()
    elif len(field) == 2:
        if "birth_year" in field and "sex" in field:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id,
                (Profile.sex == field["sex"]),
                (
                    Profile.birth_year == int(field["birth_year"])
                    if field["birth_year"].isdigit()
                    else False
                ),
            ).all()
        elif "birth_year" in field:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id,
                (Profile.race == field["race"]),
                (
                    Profile.birth_year == int(field["birth_year"])
                    if field["birth_year"].isdigit()
                    else False
                ),
            ).all()
        else:
            profile = Profile.query.filter(
                Profile.user_id_fk == user_id,
                (Profile.sex == field["sex"]),
                (Profile.race == field["race"]),
            ).all()
    elif len(field) == 3:
        profile = Profile.query.filter(
            Profile.user_id_fk == user_id,
            (Profile.sex == field["sex"]),
            (Profile.race == field["race"]),
            (
                Profile.birth_year == int(field["birth_year"])
                if field["birth_year"].isdigit()
                else False
            ),
        ).all()
    else:
        profile = Profile.query.filter_by(user_id_fk=user_id).all()
    return profile


###
# Routing for your application.
###


@app.route("/api/v1/csrf-token", methods=["GET"])
def get_csrf():
    return jsonify({"csrf_token": generate_csrf()}), 200


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/assets/<path:filename>")
def assets(filename):
    return app.send_static_file(os.path.join("assets", filename))


###
# Users
###


@app.route("/api/register", methods=["POST"])
def register():
    form = UserForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return jsonify({"error": "Username already exists!!"}), 400
        elif User.query.filter_by(email=form.email.data).first():
            return jsonify({"error": "Email Address already exists!!"}), 400
        else:
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            new_user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data,
                email=form.email.data,
                photo=filename,
            )
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id

            return jsonify(
                {
                    "message": "User registered successfully!!",
                    "user": {
                        "id": new_user.id,
                        "username": new_user.username,
                        "name": new_user.name,
                        "email": new_user.email,
                        "photo": new_user.photo,
                    },
                }
            ), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            token = create_access_token(identity=user.id)

            session["user_id"] = user.id
            login_user(user)

            return jsonify(
                {
                    "message": "Logged in successfully!!",
                    "token": token,
                    "id": user.id,
                    "user": {
                        "username": user.username,
                        "name": user.name,
                    },
                }
            ), 200
        else:
            return jsonify({"error": "Invalid username or password!!"}), 401
    else:
        return jsonify({"error": form_errors(form)}), 400


@app.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        session.pop("user_id", None)
        logout_user()
        return jsonify({"message": "Logged out successfully!!"}), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found!!"}), 404

        profiles = db.session.query(Profile).filter_by(user_id_fk=user_id).all()
        if not profiles:
            return jsonify({"error": "No profiles found for this user!!"}), 404

        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "photo": f"/api/photo/{user.photo}",
            "date_joined": user.date_joined.strftime("%Y-%m-%d"),
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
                "family_oriented": profile.family_oriented,
            }
            for profile in profiles
        ]

        return jsonify({"user": user_data, "profiles": profiles_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###
# Profiles
###


@app.route("/api/profiles", methods=["GET"])
@jwt_required()
def get_profiles():
    current_user_id = session.get("user_id")

    profiles = Profile.query.filter(Profile.user_id_fk != current_user_id).all()

    return jsonify({"profiles": [profile.serialize() for profile in profiles]}), 200


@app.route("/api/check-profiles/<int:user_id>", methods=["GET"])
@jwt_required()
def has_complete_profile(user_id):
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    status = any(p.is_complete() for p in profiles)
    if status:
        return jsonify({"status": status}), 200
    else:
        return jsonify(
            {"error": "You need to have at least one profile completed!!"}
        ), 404


@app.route("/api/profiles/<int:profile_id>", methods=["PUT"])
@jwt_required()
def update_profile(profile_id):
    form = ProfileForm()
    user_id = session.get("user_id")

    profile = Profile.query.get_or_404(profile_id)

    if profile.user_id_fk != user_id:
        return jsonify({"error": "Unauthorized!!"}), 403

    profile.description = form.description.data
    profile.parish = form.parish.data
    profile.biography = form.biography.data
    profile.sex = form.sex.data
    profile.race = form.race.data
    profile.birth_year = form.birth_year.data
    profile.height = form.height.data
    profile.fav_cuisine = form.fav_cuisine.data
    profile.fav_colour = form.fav_colour.data
    profile.fav_school_subject = form.fav_school_subject.data
    profile.political = form.political.data
    profile.religious = form.religious.data
    profile.family_oriented = form.family_oriented.data

    db.session.commit()
    return jsonify({"message": "Profile updated successfully!!"}), 200


@app.route("/api/profiles", methods=["POST"])
# @jwt_required()
def create_profile():
    form = ProfileForm()
    user_id = session.get("user_id")

    if form.validate_on_submit():
        if Profile.query.filter_by(user_id_fk=user_id).count() >= 3:
            return jsonify({"error": "Max 3 profiles allowed!!"}), 400
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
                family_oriented=form.family_oriented.data,
            )
            db.session.add(profile)
            db.session.commit()
            return jsonify({"message": "New Profile Created!!"}), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/profiles/<int:profile_id>", methods=["GET"])
@jwt_required()
def get_profile(profile_id):
    current_user_id = session.get("user_id")
    if not has_complete_profile(current_user_id):
        return jsonify({"error": "Complete your profile to access this feature!!"}), 403

    profile = Profile.query.get_or_404(profile_id)
    profile_data = {
        "id": profile.id,
        "user_id": profile.user_id_fk,
        "user_name": profile.user.name,
        "photo": f"/api/photo/{profile.user.photo}",
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
        "family_oriented": profile.family_oriented,
    }
    return jsonify({"profile": profile_data}), 200


@app.route("/api/search", methods=["GET"])
@jwt_required()
def search_profiles():
    try:
        u_id = session.get("user_id")
        search_term = request.args.get("search")
        search_field = json.loads(request.args.get("field"))
        search_field = dict(search_field)

        results = []

        if search_field:
            if not check_fields(search_field):
                return jsonify({"error": "Please fill all filter fields!!"}), 400

        if search_term:
            user_query = User.query.filter(
                User.id != u_id, (User.name.ilike(f"%{search_term}%"))
            ).all()

            if user_query:
                for user in user_query:
                    profiles = query_profile(user.id, search_field)
                    for profile in profiles:
                        profile = profile.serialize()
                        results.append(profile)
                if results != []:
                    return jsonify({"results": results}), 200
                else:
                    return jsonify({"error": "No results found!!"}), 404
            else:
                return jsonify({"error": "No profiles found!!"}), 404
        else:
            return jsonify({"error": "No search query provided!!"}), 400
    except Error as e:
        return jsonify({"error": str(e)}), 500


###
# Favourites
###


@app.route("/api/profiles/<int:user_id>/favourite", methods=["POST", "DELETE"])
@jwt_required()
def add_or_delete_favourite(user_id):
    u_id = session.get("user_id")

    if not has_complete_profile(u_id):
        return jsonify({"error": "Complete your profile to access this feature!!"}), 403

    if request.method == "DELETE":
        fav = Favourite.query.filter_by(user_id_fk=u_id, fav_user_id_fk=user_id).first()
        if not fav:
            return jsonify({"error": "User not found!!"}), 404
        else:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({"message": "User removed from favourites!!"}), 200
    else:
        if user_id == u_id:
            return jsonify({"error": "Cannot favourite yourself!!"}), 400

        profile = Profile.query.filter_by(user_id_fk=user_id).first()
        if not profile:
            return jsonify({"error": "User not found!!"}), 404

        fav = Favourite.query.filter_by(user_id_fk=u_id, fav_user_id_fk=user_id).first()
        if fav:
            return jsonify({"error": "Already added to favourites!!"}), 404

        fav = Favourite(user_id_fk=u_id, fav_user_id_fk=user_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({"message": "User added to favourites!!"}), 201


@app.route("/api/profiles/matches/<int:profile_id>", methods=["GET"])
@jwt_required()
def get_matches(profile_id):
    matches = []
    year = datetime.now().year

    current_user_id = session.get("user_id")
    if not has_complete_profile(current_user_id):
        return jsonify({"error": "Complete your profile to access this feature!!"}), 403

    profile = Profile.query.get_or_404(profile_id)

    if profile.user_id_fk != current_user_id:
        return jsonify({"error": "Unauthorized!!"}), 403

    age = year - profile.birth_year

    potential_matches = Profile.query.filter(
        Profile.id != profile.id,
        Profile.user_id_fk != current_user_id,
    ).all()

    for match in potential_matches:
        if profile.sex != match.sex:
            match_age = year - match.birth_year
            age_diff = abs(match_age - age)
            
            profile_height_split = profile.height.split("'")
            profile_ft_to_in = int(profile_height_split[0]) * 12
            profile_height = profile_ft_to_in + int(profile_height_split[1])
            
            match_height_split = match.height.split("'")
            match_ft_to_in = int(match_height_split[0]) * 12
            match_height = match_ft_to_in + int(match_height_split[1])
            
            height_diff = abs(profile_height - match_height)
            if age_diff <= 5 and 3 <= height_diff <= 10:
                fields_to_check = [
                    "fav_cuisine",
                    "fav_colour",
                    "fav_school_subject",
                    "political",
                    "religious",
                    "family_oriented",
                ]
                match_count = sum(
                    1
                    for field in fields_to_check
                    if getattr(profile, field) == getattr(match, field)
                )
               
                if match_count >= 3:
                    match_data = {
                        "id": match.id,
                        "user_id": match.user_id_fk,
                        "user_name": match.user.name,
                        "photo": f"/api/photo/{match.user.photo}",
                        "description": match.description,
                        "parish": match.parish,
                        "biography": match.biography,
                        "sex": match.sex,
                        "race": match.race,
                        "birth_year": match.birth_year,
                        "height": match.height,
                        "fav_cuisine": match.fav_cuisine,
                        "fav_colour": match.fav_colour,
                        "fav_school_subject": match.fav_school_subject,
                        "political": match.political,
                        "religious": match.religious,
                        "family_oriented": match.family_oriented,
                    }
                    matches.append(match_data)

    if matches:
        return jsonify(
            {"message": "Matches found!!", "matches": matches}
        ), 200
    else:
        return jsonify({"error": "No matches found!!"}), 404


@app.route("/api/users/<int:user_id>/favourites", methods=["GET"])
@jwt_required()
def get_user_favourites(user_id):
    order = request.args.get("order")
    favourites = (
        db.session.query(Favourite)
        .join(Profile, Favourite.fav_user_id_fk == Profile.id)
        .join(User, Profile.user_id_fk == User.id)
        .filter(Favourite.user_id_fk == user_id)
    )

    if not favourites:
        return jsonify({"error": "No favourites found for this user!!"}), 404
    else:
        if order == "name":
            favourites = favourites.order_by(User.name.asc())
        elif order == "parish":
            favourites = favourites.order_by(Profile.parish.asc())
        elif order == "age":
            favourites = favourites.order_by(Profile.birth_year.desc())
        favourites = favourites.all()
        return jsonify(
            {"favourites": [favourite.serialize() for favourite in favourites]}
        ), 200


@app.route("/api/users/favourites/<int:N>", methods=["GET"])
@jwt_required()
def get_top_favoured_users(N):
    try:
        order = request.args.get("order")

        year = datetime.now().year

        top_favourites_ids = (
            db.session.query(
                Favourite.fav_user_id_fk.label("fav_user_id"),
                func.count(Favourite.fav_user_id_fk).label("fav_count"),
            )
            .group_by(Favourite.fav_user_id_fk)
            .order_by(desc("fav_count"))
            .limit(N)
            .subquery()
        )

        top_favourites = (
            db.session.query(Profile, User)
            .select_from(top_favourites_ids)
            .join(Profile, Profile.id == top_favourites_ids.c.fav_user_id)
            .join(User, User.id == Profile.user_id_fk)
        )

        if not top_favourites:
            return jsonify({"error": "No favoured users found!!"}), 404

        else:
            if order == "name":
                top_favourites = top_favourites.order_by(User.name.asc())
            elif order == "parish":
                top_favourites = top_favourites.order_by(Profile.parish.asc())
            elif order == "age":
                top_favourites = top_favourites.order_by(Profile.birth_year.desc())
            else:
                top_favourites = top_favourites.order_by(
                    top_favourites_ids.c.fav_count.desc()
                )

            top_favourites = top_favourites.all()

            favourites_list = []
            for profile, user in top_favourites:
                favourites_list.append(
                    {
                        "fav_profile_id": profile.id,
                        "user_name": user.name,
                        "parish": profile.parish,
                        "age": year - profile.birth_year,
                    }
                )

            return jsonify({"favourites": favourites_list}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/photo/<filename>", methods=["GET"])
def get_photo(filename):
    return send_from_directory(
        os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]), filename
    ), 200


###
# The functions below should be applicable to all Flask apps.
###


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = "Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error,
            )
            error_messages.append(message)

    return error_messages


@app.route("/<file_name>.txt")
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + ".txt"
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["X-UA-Compatible"] = "IE=Edge,chrome=1"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify({"error": "Not found"}), 404
    # return render_template('404.html'), 404
