from flask import Blueprint, render_template, request,redirect, url_for,json,jsonify
from models.user import User
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token
)

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

SECRET_KEY = os.environ.get(
        'SECRET_KEY')
# app.config['SECRET_KEY'] = ''

@sessions_blueprint.route('/', methods=['POST'])
def login () :  
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.get_or_none(User.email==email)

    
    if user :
        if check_password_hash(user.password, password) :
                access_token = create_access_token(identity= user.id)
                return jsonify({"access_token":access_token,
                                "username" : user.username,
                                "email": user.email,
                                "id":user.id,
                                "profilepic":user.profilepic_url,
                                "bio":user.bio}),200
        return jsonify(message="Wrong Password")
    return jsonify(message='Email Address Does Not Exist')
    

