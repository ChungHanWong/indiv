from flask import Blueprint, render_template, request,redirect, url_for,json,jsonify
from flask_cors import CORS
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/', methods=['POST'])
def signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    hashed = generate_password_hash(password)
    user_database = User.select()
    for u in user_database :
        if username == u.username :
            return jsonify(message="Username Already Exists")
        elif email == u.email :
            return jsonify(message="Email Already Exists")
    user = User.create(username=username,email=email,password=hashed)
    user_logged_in = User.get_or_none(User.username==username)
    if user :
        access_token = create_access_token(identity= user_logged_in.id)
        return jsonify({"access_token":access_token,
                        "username" : user_logged_in.username,
                        "email": user_logged_in.email,
                        "id":user_logged_in.id,
                        "profilepic":user_logged_in.profilepic_url,
                        "bio":user_logged_in.bio,
                        "message": "Successfully Signed Up"}),200
    