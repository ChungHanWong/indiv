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


sold_blueprint = Blueprint('sold',
                            __name__,
                            template_folder='templates')

@sold_blueprint.route('/', methods=['POST'])
def sold () :
    
    pic_id = request.form.get('id')
    
    picture = Picture.get(Picture.id == pic_id)
    
    picture.buyer_id = picture.bidder_id
    picture.sold = True
    picture.save()
    return jsonify(message="You Have Accepted the Bidder's Offer")
    