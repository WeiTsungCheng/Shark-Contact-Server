from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from db import db

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, AdminUserRegister
from resources.addressbook import AddressBook
from resources.contactItem import ContactItem, ContactItemList

import os
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_HOST")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = os.getenv('SECRET_KEY')
api = Api(app)

load_dotenv()

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<uuid:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, "/logout")
api.add_resource(AddressBook, "/user/addressbook/<string:bookname>")
api.add_resource(ContactItem, "/user/addressbook/<string:bookname>/contactitem/<string:itemname>")
api.add_resource(ContactItemList, "/user/addressbook/<string:bookname>/contactitems")
api.add_resource(AdminUserRegister, "/admin/register")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8069, debug=True)