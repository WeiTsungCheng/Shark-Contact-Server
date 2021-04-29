
from models.user import UserModel
from flask_restful import Resource, reqparse

class UserModel(db.Model):
    __tablename__ = "users"

    name = ""
    addressbooks = "" [contactitem]
    contact = "" contactitem
	
    def __init__(self, name):
        self.name = name 

    