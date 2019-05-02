from flask import Blueprint, render_template, request,redirect, url_for,json,jsonify,make_response
from models.picture import Picture
from models.user import User
from helper import *
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS

paintings_blueprint = Blueprint('paintings',
                            __name__,
                            template_folder='templates')


@paintings_blueprint.route('/paintingsubmit', methods=['POST'])
def paintingsubmit():
    name = request.form.get('name')
    category = request.form.get('category')
    description = request.form.get('description')
    userid = request.form.get('id')
    file = request.files["picture"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        picture = Picture.create(name=name,description=description,category=category,image=file.filename,artist_id=userid)
    return make_response('Artwork Submitted')



@paintings_blueprint.route('/offer', methods=['GET'])
def offer():
    allpic = Picture.select()
    pics_info= []
    for a in allpic :
        picpic = {}
        picpic['name'] = a.name
        picpic['category'] = a.category
        picpic['description'] = a.description
        paint = Picture.get(Picture.name == a.name).profilepic_url
        picpic['image'] = paint
        picpic['id'] = a.id
        pics_info.append(picpic)

    return jsonify(pics_info)

@paintings_blueprint.route('/offer/<id>', methods=['GET'])
def detail(id):
    a = Picture.get(Picture.id == id)
    artist = a.artist_id
    user = User.get(User.id== artist)
    artist_name = user.username
    picpic = {}
    picpic['name'] = a.name
    picpic['category'] = a.category
    picpic['description'] = a.description
    paint = Picture.get(Picture.name == a.name).profilepic_url
    picpic['image'] = paint
    picpic['price'] = a.price
    picpic['artist'] = artist_name
    picpic['artist_id'] = str(artist)
    picpic['sold'] = a.sold
    return jsonify(picpic)

@paintings_blueprint.route('/bid', methods=['POST'])
def bid () :
    description = request.form.get('description')
    price = request.form.get('price')
    bidprice= int(price)
    user_id = request.form.get('id')
    pic = Picture.get(Picture.description==description)
    currentprice = int(pic.price)
    if currentprice < bidprice :
        pic.price = price
        pic.bidder_id = user_id
        pic.save()
        return jsonify (message= "You are currently the highest bidder")
    else :
        return jsonify(message= "You are not the highest bidder")
    
    
@paintings_blueprint.route('/delete', methods=['POST'])
def delete () :
    pic_id = request.form.get('id')
    picture = Picture.get(Picture.id == pic_id)
    picture.delete_instance()
    return jsonify (message="Artwork Deleted")


