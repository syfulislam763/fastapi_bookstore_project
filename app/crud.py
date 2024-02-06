from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.sql import text
from .exception import UnicornException, TestException
from . import models, schemas




def create_book(payload:schemas.BookModel, db:Session):
    book = models.Books(id=payload.id,title=payload.title,author=payload.author, genre=payload.genre, price=payload.price)

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(id:int, db:Session):
    book =  db.query(models.Books).filter(models.Books.id == id).first()
    if book is None:
        raise UnicornException(id=id)
    return book

def get_books(db:Session):
    books = db.query(models.Books).all()
    return books

def update_book(id:int,payload:schemas.UpdateBook, db:Session):
    book = db.query(models.Books).filter(models.Books.id == id).first()
    if id == 10:
        raise TestException(id=id, msg="My custom message!")
    if book is None:
        raise UnicornException(id=id)
    
    if payload.title:
        book.title = payload.title
    if payload.author:
        book.author = payload.author

    if payload.genre:
        book.genre = payload.genre
    
    if payload.price:
        book.price = payload.price

    
    db.commit()
    db.refresh(book)

    return book
