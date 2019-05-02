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


@sold_blueprint.route('/purchase', methods=['GET'])
@jwt_required
def purchase () :
    current_user = get_jwt_identity()
    purchased_artwork = Picture.select().where(Picture.buyer_id==current_user)
    bidding_artwork = Picture.select().where((Picture.bidder_id== current_user) & (Picture.buyer_id == None) )
    purchased_info = []
    for p in purchased_artwork : 
        art_art = {}
        art_art['name'] = p.name
        art_art['category'] = p.category
        art_art['description'] = p.description
        art = Picture.get(Picture.name == p.name).profilepic_url
        art_art['image'] = art
        art_art['id'] = p.id
        art_art['price'] = p.price
        art_art['paid'] = p.paid
        purchased_info.append(art_art)
    
    bidding_info = []

    for b in bidding_artwork :
        bid_bid = {}
        bid_bid['name'] = b.name
        bid_bid['category'] = b.category
        bid_bid['description'] = b.description
        art = Picture.get(Picture.name == b.name).profilepic_url
        bid_bid['image'] = art
        bid_bid['id'] = b.id
        bid_bid['price'] = b.price
        bid_bid['paid'] = b.paid
        bidding_info.append(bid_bid)


    return jsonify(purchase=purchased_info, bid =bidding_info)

@sold_blueprint.route('/paid', methods=['POST'])
def paid () :
    pic_id = request.form.get('id')
    picture = Picture.get(Picture.id == pic_id)
    picture.paid = True
    
    picture.save()
    return jsonify(message="You Purchased the Artwork!")
    