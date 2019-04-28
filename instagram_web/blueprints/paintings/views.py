from flask import Blueprint, render_template, request,redirect, url_for,json,jsonify,make_response
from models.picture import Picture
from helper import *
from werkzeug.utils import secure_filename
from models.picture import Picture
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
    picpic = {}
    picpic['name'] = a.name
    picpic['category'] = a.category
    picpic['description'] = a.description
    paint = Picture.get(Picture.name == a.name).profilepic_url
    picpic['image'] = paint
    picpic['price'] = a.price
    return jsonify(picpic)
    
    




