
from db import db

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from werkzeug.security import generate_password_hash

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), default=lambda: uuid4(), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    pwd_hash = db.Column(db.String(240), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    addressbook = db.relationship('AddressBookModel', back_populates='user', uselist=False, passive_deletes=True)

    identity = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)

    @property
    def password(self):
        raise AttributeError('can not read password property')

    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password, 'sha256')

    def __init__(self, username, password, identity, phone_number, is_admin=False):
        self.username = username
        self.password = password
        self.identity = identity
        self.phone_number = phone_number
        self.is_admin = is_admin

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):

        return {
            'id': str(self.id),
            'username': self.username,
            'identity': self.identity,
            'phone_number': self.phone_number,
            'addressbook_name': self.addressbook.bookname if self.addressbook else None
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query.filter_by(identity=identity).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

