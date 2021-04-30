
from db import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class AddressBookModel(db.Model):
    __tablename__ = "addressbooks"
    id = db.Column(UUID(as_uuid=True), default=lambda: uuid4().hex, primary_key=True)
    bookname = db.Column(db.String(80))

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def _init__(self, bookname, user_id):
        self.bookname = bookname
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'name': self.bookname,
            'user_id': self.user_id
        }