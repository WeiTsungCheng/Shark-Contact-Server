
from models.addressbook import AddressBookModel
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

# class AddressBook(Resource):

