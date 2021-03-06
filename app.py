from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from db import db

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.addressbook import AddressBook
from resources.contactItem import ContactItem, ContactItemList

import os
from dotenv import load_dotenv
from blacklist import BLACKLIST

app = Flask(__name__)
# 切記要先 load 才取得到 .env 的資料
load_dotenv()

# 如果從 Heroku 上拿不到環境變數則取本地端的 Server 位置
# 因為 .env 並不會上傳到 Github 上

if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_HOST")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# 如果從 Heroku 上拿不到環境變數則取本地端的 SECRET_KEY 位置
# 因為 .env 並不會上傳到 Github 上
# 另外 secret_key 一定要設, 因為做為 flask-jwt-extended 加密的鹽

if os.environ.get('SECRET_KEY'):
    app.secret_key = os.environ.get('SECRET_KEY')
else:
    app.secret_key = os.getenv('SECRET_KEY')

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    print(jwt_payload['jti'])
    return jwt_payload['jti'] in BLACKLIST

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/info')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, "/logout")
api.add_resource(AddressBook, "/user/addressbook/<string:bookname>")
api.add_resource(ContactItem, "/user/addressbook/<string:bookname>/contactitem/<string:itemname>")
api.add_resource(ContactItemList, "/user/addressbook/<string:bookname>/contactitems")


if __name__ == '__main__':
    db.init_app(app)
    # debug 設為 True 可以存擋後可以自動 reload , 不用重啟 Server , 但是要使用 VS code debug 需設為 False
    app.run(port=8069, debug=False)