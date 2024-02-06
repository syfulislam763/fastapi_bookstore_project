from .database import Base
from sqlalchemy import Column, Integer, Float, String


class Books(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    author = Column(String(30))
    genre = Column(String(30))
    price = Column(Float)


