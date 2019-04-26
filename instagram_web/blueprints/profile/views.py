from flask import Blueprint, render_template, request,redirect, url_for,json,jsonify
from models.user import User
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from helper import *
from werkzeug.utils import secure_filename


profile_blueprint = Blueprint('profile',
                            __name__,
                            template_folder='templates')

@profile_blueprint.route('/', methods=['GET'])
@jwt_required
def profile () :
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200