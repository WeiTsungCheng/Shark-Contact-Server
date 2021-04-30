from flask import Flask, jsonify
from flask_restful import Api

from flask_jwt_extended import JWTManager

from db import db

from resources.user import UserRegister, User, UserLogin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5435/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "wei76"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

# @app.route('/test')
# def index():
#     sql_cmd = """
#         select * from public.users
#         """
#     query_data = db.engine.execute(sql_cmd)
#     print(query_data)
#     return 'ok'

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<uuid:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8069, debug=True)