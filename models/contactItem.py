
from db import db

class ContactItemModel(db.Model):
    __tablename__ = "contactitem"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    identity = db.Column(db.String(80))
    phonenumber =  db.Column(db.String(20))

    def __init__(self, name, identity, phonenumber):
        self.name = name 
        self.identity = identity
        self.phonenumber = phonenumber

