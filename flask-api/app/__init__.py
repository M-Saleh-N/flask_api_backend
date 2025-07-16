from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration from config file
    app.config.from_object('app.config.Config')

    # Initialize database
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # Initialize Flask-RESTful API
    api = Api(app)

    # Import resources (make sure __init__.py exists in each module folder)
    from app.resources.user import UserListResource, UserResource
    from app.resources.contact import ContactListResource, ContactResource
    from app.resources.product import ProductListResource, ProductResource

    # Register API endpoints
    # User resources
    api.add_resource(UserListResource, '/v1/users')
    api.add_resource(UserResource, '/v1/users/<int:user_id>')

    # Contact resources
    api.add_resource(ContactListResource, '/v1/contacts')
    api.add_resource(ContactResource, '/v1/contacts/<int:user_id>')

    # Product resources
    api.add_resource(ProductListResource, '/v1/products')
    api.add_resource(ProductResource, '/v1/products/<int:product_id>')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
