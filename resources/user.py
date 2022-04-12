
from sqlalchemy.dialects.postgresql.base import UUID
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
import datetime

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from blacklist import BLACKLIST

from models.user import UserModel
from distutils.util import strtobool

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('is_admin',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('adminkey',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('identity',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('phone_number',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )

import os

class UserRegister(Resource):

    def post(self):

        data = _user_parser.parse_args()

        if (not data['identity']) or (not data['phone_number']):
            return {"message": "identity and phone_number must be provided"}, 400

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.find_by_identity(data['identity']):
            return {"message": "A user with that identity already exists"}, 400

        user = UserModel(data['username'], data['password'], data['identity'], data['phone_number'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

# class AdminUserRegister(Resource):

#     def post(self):
#         data = _user_parser.parse_args()

#         if (not data['identity']) or (not data['phone_number']):
#            return {"message": "identity and phone_number must be provided"}, 400

#         if UserModel.find_by_username(data['username']):
#             return {"message": "A user with that username already exists"}, 400

#         if os.getenv('ADMIN_USER_KEY') != data['adminkey']:
#             return {"message": "Can't Register"}, 401

#         user = UserModel(data['username'], data['password'], data['identity'], data['phone_number'], strtobool(data["is_admin"]))
#         user.save_to_db()

#         return {"message": "Admin created successfully."}, 201

class User(Resource):

    @jwt_required()
    def get(self):
        jwt_user_id = get_jwt_identity()
        jwt_user = UserModel.find_by_id(jwt_user_id)

        if not jwt_user:
            return {'message': 'User Not Found'}, 404

        return jwt_user.json(), 200

    @jwt_required()
    def delete(self):
        jwt_user_id = get_jwt_identity()
        jwt_user = UserModel.find_by_id(jwt_user_id)

        if not jwt_user:
            return {'message': 'User Not Found'}, 404

        jwt_user.delete_from_db()

        return {'message': 'User deleted.'}, 200
    # @jwt_required()
    # def get(self, user_id):
    #     jwt_user_id = get_jwt_identity()
    #     jwt_user = UserModel.find_by_id(jwt_user_id)

    #     if (not jwt_user.is_admin) and (jwt_user.id != user_id):
    #         return {'message': 'Only Admin and Self can get User'}, 401

    #     user = UserModel.find_by_id(user_id)
    #     if not user:
    #         return {'message': 'User Not Found'}, 404

    #     return user.json(), 200

    # @jwt_required()
    # def delete(self, user_id):
    #     jwt_user_id = get_jwt_identity()
    #     jwt_user = UserModel.find_by_id(jwt_user_id)

    #     if (not jwt_user.is_admin) and (jwt_user.id != user_id):
    #         return {'message': 'Only Admin and Self can delete User'}, 401

    #     user = UserModel.find_by_id(user_id)
    #     if not user:
    #         return {'message': 'User Not Found'}, 404

    #     user.delete_from_db()
    #     return {'message': 'User deleted.'}, 200


class UserLogin(Resource):

    @classmethod
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and check_password_hash(user.pwd_hash, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=datetime.timedelta(days=1))
            refresh_token = create_refresh_token(user.id)
            return {
                'user_id': str(user.id),
                'token': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, 200

        return {"message": "Invalid Credentials!"}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):

        jti = get_jwt()['jti']
        BLACKLIST.add(jti)

        return {"message": "Successfully logout out"}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False, expires_delta=datetime.timedelta(days=1))
        return {
            "token": {"access_token": new_token}
        }, 200