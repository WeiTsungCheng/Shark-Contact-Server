
from sqlalchemy.dialects.postgresql.base import UUID
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

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

import os

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class AdminUserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if os.getenv('ADMIN_USER_KEY') != data['adminkey']:
            return {"message": "Can't Register"}, 401

        user = UserModel(data['username'], data['password'], strtobool(data["is_admin"]))
        user.save_to_db()

        return {"message": "Admin created successfully."}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404

        return user.json(), 200

    @classmethod
    def delete(cls, user_id):

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404

        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):

    @classmethod
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and check_password_hash(user.pwd_hash, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
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
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200