
from models.user import UserModel
from db import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

g = UserModel(username="william", password=123)
print(g.id)
print(g.password)
# import uuid
# print(uuid4().hex)
# from postgreql import text
# from postgreql import text

# print(db.text("gen_random_uuid()"))

# print(Column(UUID, server_default=db.text("gen_random_uuid()")