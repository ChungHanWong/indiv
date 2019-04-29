from flask import Blueprint, render_template, request,redirect, url_for,jsonify
from models.user import User
from models.picture import Picture
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from helper import *
from werkzeug.utils import secure_filename
import json


profile_blueprint = Blueprint('profile',
                            __name__,
                            template_folder='templates')

@profile_blueprint.route('/', methods=['GET'])
@jwt_required
def profile () :
    current_user = get_jwt_identity()
    
    allpic = Picture.select().where(Picture.artist_id==current_user)
    pics_info= []
    for a in allpic :
        picpic = {}
        picpic['name'] = a.name
        picpic['category'] = a.category
        picpic['description'] = a.description
        paint = Picture.get(Picture.name == a.name).profilepic_url
        picpic['image'] = paint
        picpic['id'] = a.id
        picpic['price'] = a.price
        pics_info.append(picpic)

    return jsonify(pics_info)


@profile_blueprint.route('/edit', methods=['POST'])
def editprofile () :
    file = request.files["picture"]
    username = request.form.get('username')
    
    # user= User.get(User.username==username)
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        
        user = User.get(User.username==username)
        
        user.profilepic = file.filename
        user.save()
        # q = (User
        # .update({User.profilepic: file.filename})
        # .where(User.username == username))
        # q.execute() 
        profilepic = user.profilepic_url
        
        return jsonify(profilepic = user.profilepic_url)

    pass

@profile_blueprint.route('/editbio', methods=['POST'])
def editbio() :
    username = request.form.get('username')
    bio = request.form.get('bio')
    user = User.get(User.username==username)
    user.bio  = bio
    user.save()
    return jsonify(bio = user.bio)