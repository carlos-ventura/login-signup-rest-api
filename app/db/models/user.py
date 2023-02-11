from sqlalchemy import Column, String

from app.db.config import Base


class User(Base):
    __tablename__ = 'user'

    username = Column(String, primary_key=True)
    fullname = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
