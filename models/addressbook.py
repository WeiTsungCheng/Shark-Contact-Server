
from models.contactItem import ContactItemModel
from db import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class AddressBookModel(db.Model):
    __tablename__ = "addressbooks"
    id = db.Column(UUID(as_uuid=True), default=lambda: uuid4(), primary_key=True)
    bookname = db.Column(db.String(80))

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), unique=True)
    user = db.relationship('UserModel', back_populates="addressbook")

    contactitems = db.relationship('ContactItemModel', back_populates='addressbook', uselist=True)

    def __init__(self, bookname, user_id):
        self.bookname = bookname
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):

        return {
            'id': self.id.hex,
            'bookname': self.bookname,
            'contactitems': [item.json() for item in ContactItemModel.find_by_bookid(self.id)]
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

