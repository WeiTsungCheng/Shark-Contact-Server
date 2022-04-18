from models.contactItem import ContactItemModel
from flask_restful import Resource, reqparse

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.user import UserModel
from models.contactItem import ContactItemModel

_contact_parser = reqparse.RequestParser()

_contact_parser.add_argument('itemname',
                          type=str,
                          required=False,
                          help="This field can not be blank."
                          )

_contact_parser.add_argument('identity',
                          type=str,
                          required=True,
                          help="This field can not be blank."
                          )

_contact_parser.add_argument('phonenumber',
                          type=str,
                          required=True,
                          help="This field can not be blank."
                          )

class ContactItem(Resource):

    @jwt_required()
    def get(self, bookname, itemname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        addressbook_name = user.addressbook.bookname if user.addressbook else None
        if addressbook_name != bookname:
            return {'message': 'Addressbook name not found'}, 404

        contactitems = user.addressbook.contactitems
        contactItem = list(filter(lambda item: item.itemname == itemname, contactitems))

        if contactItem:
            return contactItem[0].json()
        return {'message': 'ContactItem not found'}, 404

    @jwt_required()
    def post(self, bookname, itemname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        addressbook_name = user.addressbook.bookname if user.addressbook else None
        if addressbook_name != bookname:
            return {'message': 'Addressbook name not found'}, 404

        addressbook_id = user.addressbook.id if user.addressbook else None
        data = _contact_parser.parse_args()

        contactItem = ContactItemModel.find_by_bookid_and_name(addressbook_id, itemname)

        if contactItem:
            return {'message': "An contactItem already exists."}, 400
        else:
            contactItem = ContactItemModel(itemname, data['identity'], data['phonenumber'], addressbook_id)

        try:
            contactItem.save_to_db()
        except Exception as e:
            return {"message": "An error occurred inserting the contactItem. '{}'".format(e)}, 500

        return contactItem.json(), 201

    @jwt_required()
    def delete(self, bookname, itemname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        addressbook_name = user.addressbook.bookname if user.addressbook else None
        if addressbook_name != bookname:
            return {'message': 'Addressbook name not found'}, 404

        contactitems = user.addressbook.contactitems
        contactItem = list(filter(lambda item: item.itemname == itemname, contactitems))

        if contactItem:
            contactItem[0].delete_from_db()
            return {'message': 'ContactItem deleted'}, 200
        return {'message': 'ContactItem not found'}, 404

    @jwt_required()
    def put(self, bookname, itemname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user == None:
            return  {'message': 'User not found'}, 404

        addressbook_name = user.addressbook.bookname if user.addressbook else None
        if addressbook_name != bookname:
            return {'message': 'Addressbook name not found'}, 404

        addressbook_id = user.addressbook.id if user.addressbook else None
        data = _contact_parser.parse_args()

        newContactItem = ContactItemModel.find_by_bookid_and_name(addressbook_id, data['itemname'])
        if newContactItem:
            return {'message': "An contactItem already exists."}, 400

        contactItem = ContactItemModel.find_by_bookid_and_name(addressbook_id, itemname)

        if contactItem:

            if contactItem.itemname == itemname:
                contactItem.itemname = data['itemname']
                contactItem.identity = data['identity']
                contactItem.phonenumber = data['phonenumber']
            else:
                return {'message': 'ContactItem not found'}, 404

        else:
            contactItem = ContactItemModel(itemname, data['identity'], data['phonenumber'], addressbook_id)

        try:
            contactItem.save_to_db()
        except Exception as e:
            return {"message": "An error occurred inserting the contactItem. '{}'".format(e)}, 500

        return contactItem.json(), 201


class ContactItemList(Resource):

    @jwt_required()
    def get(self, bookname):

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        addressbook_name = user.addressbook.bookname if user.addressbook else None
        if addressbook_name != bookname:
            return {'message': 'Addressbook name not found'}, 404

        contactitems = user.addressbook.contactitems

        return {'contactitems': [item.json() for item in contactitems]}, 200
