
from sqlalchemy.dialects.postgresql.base import UUID
from models.contactItem import ContactItemModel
from flask_restful import Resource, reqparse
import uuid

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.contactItem import ContactItemModel

_contact_parser = reqparse.RequestParser()

_contact_parser.add_argument('itemname',
                          type=str,
                          required=False,
                          help="This field can be blank."
                          )

_contact_parser.add_argument('identity',
                          type=str,
                          required=False,
                          help="This field can be blank."
                          )

_contact_parser.add_argument('phonenumber',
                          type=str,
                          required=False,
                          help="This field can be blank."
                          )


class ContactItem(Resource):

    @jwt_required()
    def get(self, addressbook_id):

        user_id = get_jwt_identity()
        contactItem = ContactItemModel.find_by_addressbook_id(addressbook_id)
        if contactItem:
            return contactItem.json()
        return {'message': 'ContactItem not found'}, 404

