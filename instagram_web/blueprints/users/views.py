from flask import Blueprint, render_template, request,redirect, url_for,json
from flask_cors import CORS
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/', methods=['POST'])
def signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    hashed = generate_password_hash(password)
    user = User.create(username=username,email=email,password=hashed)
    return "yay"