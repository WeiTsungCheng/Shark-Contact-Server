

from models.user import UserModel
from db import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# import uuid
print(uuid4())
print(type(uuid4()))
print(uuid4().hex)
print(type(uuid4().hex))
# from postgreql import text
# from postgreql import text

# print(db.text("gen_random_uuid()"))

# print(Column(UUID, server_default=db.text("gen_random_uuid()")