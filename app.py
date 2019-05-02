import os
import config
from flask import Flask
from models.base_model import db
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'indiv_web')

app = Flask('INDIV', root_path=web_dir)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'Vienna2015*'
jwt = JWTManager(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
