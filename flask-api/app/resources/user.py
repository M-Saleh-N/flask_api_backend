from flask_restful import Resource, reqparse
from app.models.user import User
from app import db
import bcrypt

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, required=True, help="First name is required")
parser.add_argument('last_name', type=str, required=True, help="Last name is required")
parser.add_argument('email', type=str, required=True, help="Email is required")
parser.add_argument('password', type=str, required=True, help="Password is required")

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return {user.id: user.to_dict() for user in users}, 200

    def post(self):
        args = parser.parse_args()
        hashed = bcrypt.hashpw(args['password'].encode(), bcrypt.gensalt())
        user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        return {user.id: user.to_dict()}, 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return {user.id: user.to_dict()}, 200

    def put(self, user_id):
        args = parser.parse_args()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        db.session.commit()
        return {user.id: user.to_dict()}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return '', 204
