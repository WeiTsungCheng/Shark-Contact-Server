
from sqlalchemy.dialects.postgresql.base import UUID
from models.addressbook import AddressBookModel
from flask_restful import Resource, reqparse
import uuid

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.addressbook import AddressBookModel

_address_parser = reqparse.RequestParser()

_address_parser.add_argument('bookname',
                          type=str,
                          required=False,
                          help="This field can be blank."
                          )

class AddressBook(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        addressbook = AddressBookModel.find_by_user_id(user_id)
        if addressbook:
            return addressbook.json()
        return {'message': 'Addressbook not found'}, 404

    @jwt_required()
    def post(self):

        user_id = get_jwt_identity()
        addressbook = AddressBookModel.find_by_user_id(user_id)

        if addressbook:
            return {'message': "An addressbook with name '{}' already exists.".format(addressbook.bookname)}, 400

        data = _address_parser.parse_args()
        addressbook = AddressBookModel(data['bookname'], uuid.UUID(user_id))

        try:
            addressbook.save_to_db()
        except Exception as e:
            return {"message": "An error occurred inserting the addressBook. '{}'".format(e)}, 500

        return addressbook.json(), 201

    @jwt_required()
    def delete(self):

        user_id = get_jwt_identity()
        addressbook = AddressBookModel.find_by_user_id(user_id)

        if addressbook:
            addressbook.delete_from_db()
            return {'message': 'addressbook deleted.'}
        return {'message': 'addressbook not found.'}, 404

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        addressbook = AddressBookModel.find_by_user_id(user_id)

        data = _address_parser.parse_args()

        if addressbook:
            addressbook.bookname = data['bookname']
        else:
            data = _address_parser.parse_args()
            addressbook = AddressBookModel(data['bookname'], uuid.UUID(user_id))

        addressbook.save_to_db()

        return addressbook.json()
