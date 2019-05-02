from app import app
from flask_cors import CORS
from flask import render_template

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from indiv_web.blueprints.users.views import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')


