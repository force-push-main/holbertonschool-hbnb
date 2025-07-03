from flask import Flask
from flask_restx import Api
"""made a slight change to import config at the top instead of when declaring a default arg like the instructions say"""
from config import DevelopmentConfig 
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# db = SQLAlchemy()
"""
instructions say to initialise db here ^^^ and then db.init(app) in the create app function
but the actual docs say to initialise db in models, import it in the create app and
then db.init_app(app)
doing it the way they say creates circular dependency warnings so don't know what the hell
the javier is smoking. lets just try it the way the docs say and then we can go from there
"""

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    from app.persistence.repository import db
    db.init_app(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app