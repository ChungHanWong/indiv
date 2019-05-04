from flask import Blueprint, render_template, request,redirect, url_for,jsonify
from models.user import User
from models.picture import Picture
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
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
        picpic['sold'] = a.sold
        if a.bidder_id :
            user = User.get(User.id == a.bidder_id)
            picpic['bidder_name'] = user.username
            pics_info.append(picpic)
        else:
            picpic['bidder_name'] = "None"
            pics_info.append(picpic)


    # purchased_artwork = Picture.select().where(Picture.buyer_id==current_user)
    # purchased_info = []
    # for p in purchased_artwork :
    #     art_art = {}
    #     art_art['name'] = p.name
    #     art_art['category'] = p.category
    #     art_art['description'] = p.description
    #     art = Picture.get(Picture.name == p.name).profilepic_url
    #     art_art['image'] = art
    #     art_art['id'] = p.id
    #     art_art['price'] = p.price
    #     purchased_info.append(art_art)

    return jsonify(artwork=pics_info)


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



@profile_blueprint.route('/others/<id>', methods=['GET'])
def otherprofiles(id):
    user = User.get(User.id == id)
    
    allinfo = {}
    allinfo['username'] = user.username
    allinfo['bio'] = user.bio
    allinfo['profilepic'] = user.profilepic_url
    
    allpic = Picture.select().where(Picture.artist_id==id)
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
        picpic['sold'] = a.sold
        if a.bidder_id :
            user = User.get(User.id == a.bidder_id)
            picpic['bidder_name'] = user.username
            pics_info.append(picpic)
        else:
            picpic['bidder_name'] = "None"
            pics_info.append(picpic)

    allinfo['artwork'] = pics_info
    
    return jsonify(allinfo)