
from models.user import UserModel
from models.addressbook import AddressBookModel
from flask_restful import Resource, reqparse
import uuid

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.addressbook import AddressBookModel

_address_parser = reqparse.RequestParser()

class AddressBook(Resource):

    @jwt_required()
    def get(self, bookname):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        addressbook = user.addressbook

        if addressbook:
            if addressbook.bookname == bookname:
                return addressbook.json()

        return {'message': 'Addressbook not found'}, 404

    @jwt_required()
    def post(self, bookname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        addressbook = user.addressbook

        if addressbook:
            return {'message': "An addressbook already exists."}, 400

        addressbook = AddressBookModel(bookname, uuid.UUID(user_id))

        try:
            addressbook.save_to_db()
        except Exception as e:
            return {"message": "An error occurred inserting the addressBook. '{}'".format(e)}, 500

        return addressbook.json(), 201

    @jwt_required()
    def delete(self, bookname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        addressbook = user.addressbook
        if addressbook:
            if addressbook.bookname == bookname:
                addressbook.delete_from_db()
                return {'message': 'addressbook deleted.'}, 200

        return {'message': 'addressbook not found.'}, 404

    @jwt_required()
    def put(self, bookname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        addressbook = user.addressbook

        if addressbook:
            addressbook.bookname = bookname
        else:
            addressbook = AddressBookModel(bookname, uuid.UUID(user_id))

        addressbook.save_to_db()

        return addressbook.json()
