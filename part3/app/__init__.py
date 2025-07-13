from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

# Instances globales des extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)

    # Charger la configuration
    app.config.from_object(DevelopmentConfig)

    # Initialiser les extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Initialiser l'API RESTx
    api = Api(
        app, 
        version='1.0',
        title='HBnB API',
        description='HBnB project',
        doc='/api/v1/'
    )
    from app.api.v1.user import api as users_ns
    from app.api.v1.amenity import api as amenty_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_n

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenty_ns, path='/api/v1/amenty')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_n, path='/api/v1/auth')

    return app