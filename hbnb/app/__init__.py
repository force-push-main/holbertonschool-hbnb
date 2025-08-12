from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from config import DevelopmentConfig 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
from app.persistence.repository import db

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, origins='*')
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app