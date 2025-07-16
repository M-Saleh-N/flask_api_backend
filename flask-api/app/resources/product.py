from flask_restful import Resource, reqparse
from app.models.product import Product
from app import db

# Parser for POST requests
product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True, help="Name is required")
product_parser.add_argument('price', type=float, required=False)
product_parser.add_argument('quantity', type=int, required=True, help="Quantity is required")
product_parser.add_argument('category', type=str, required=False)

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return {product.id: product.to_dict() for product in products}, 200

    def post(self):
        args = product_parser.parse_args()
        product = Product(
            name=args['name'],
            price=args.get('price'),
            quantity=args['quantity'],
            category=args.get('category')
        )
        db.session.add(product)
        db.session.commit()
        return {product.id: product.to_dict()}, 201

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        return {product.id: product.to_dict()}, 200
