from app import app
from flask import render_template
from indiv_api.blueprints.paintings.views import paintings_blueprint
from indiv_api.blueprints.users.views import users_blueprint
from indiv_api.blueprints.sessions.views import sessions_blueprint
from indiv_api.blueprints.profile.views import profile_blueprint
from indiv_api.blueprints.braintree.views import braintree_blueprint
from indiv_api.blueprints.sold.views import sold_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(paintings_blueprint, url_prefix="/paintings")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(profile_blueprint, url_prefix="/profile")
app.register_blueprint(braintree_blueprint, url_prefix="/braintree")
app.register_blueprint(sold_blueprint, url_prefix="/sold")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route("/")
def home():
    return render_template('home.html')