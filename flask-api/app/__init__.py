from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    from app.resources.user import UserListResource, UserResource
    from app.resources.contact import ContactListResource, ContactResource
    from app.resources.product import ProductListResource, ProductResource


    CORS(app)
    
    api = Api(app)

    # user resources
    api.add_resource(UserListResource, '/v1/users')
    api.add_resource(UserResource, '/v1/users/<int:user_id>')

    # contact resources
    api.add_resource(ContactListResource, '/v1/contacts')
    api.add_resource(ContactResource, '/v1/contacts/<int:user_id>')

    # product resources
    api.add_resource(ProductListResource, '/v1/products')
    api.add_resource(ProductResource, '/v1/products/<int:product_id>')


    with app.app_context():
        db.create_all()

    return app
