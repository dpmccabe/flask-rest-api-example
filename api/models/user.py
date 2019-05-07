from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from api.lib.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return '<Person %s: %s>' % (self.id, self.name)
