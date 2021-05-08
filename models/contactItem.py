
from db import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class ContactItemModel(db.Model):
    __tablename__ = "contactitems"
    id = db.Column(UUID(as_uuid=True), default=lambda: uuid4(), primary_key=True)
    itemname = db.Column(db.String(80))
    identity = db.Column(db.String(80))
    phonenumber =  db.Column(db.String(20))

    addressbook_id = db.Column(UUID(as_uuid=True), db.ForeignKey('addressbooks.id', ondelete='CASCADE'))
    addressbook = db.relationship('AddressBookModel', back_populates="contactitems")

    def __init__(self, itemname, identity, phonenumber, addressbook_id):
        self.itemname = itemname
        self.identity = identity
        self.phonenumber = phonenumber
        self.addressbook_id = addressbook_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):

        return {
            'id': str(self.id),
            'itemname': self.itemname,
            'identity': self.identity,
            'phonenumber': self.phonenumber
        }

    @classmethod
    def find_by_bookid(cls, _addressbook_id):
        return cls.query.filter_by(addressbook_id=_addressbook_id)

    @classmethod
    def find_by_bookid_and_name(cls, _addressbook_id, _itemname):
        return cls.query.filter_by(addressbook_id=_addressbook_id, itemname=_itemname).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

