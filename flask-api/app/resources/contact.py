from flask_restful import Resource, reqparse
from app.models.contact import Contact
from app import db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Name is required")
parser.add_argument('email', type=str, required=True, help="Email is required")
parser.add_argument('message', type=str, required=True, help="Message is required")

class ContactListResource(Resource):
    def get(self):
        contacts = Contact.query.all()
        return {contact.id: contact.to_dict() for contact in contacts}, 200

    def post(self):
        args = parser.parse_args()

        contact = Contact(
            name=args['name'],
            email=args['email'],
            message=args['message']
        )

        db.session.add(contact)
        db.session.commit()
        return {contact.id: contact.to_dict()}, 201

class ContactResource(Resource):
    def get(self, user_id):
        contact = Contact.query.get(user_id)
        if not contact:
            return {'message': 'Message not found'}, 404
        return {contact.id: contact.to_dict()}, 200