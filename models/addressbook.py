
import sqlite3
from db import db

class AddressBookModel(db.Model):
    __tablename__ = "addressbooks"
    name = db.Column(db.String(80))
    key = db.Column(db.String(80))
    createuser = ""

    def _init__(name, key):
        self.name = name 
        self.key = key
    