from pydantic import BaseModel
from typing import Optional, List




class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    price: float | None = None

    class Config:
        orm_mode = True

class BookModel(BaseModel):
    id:int
    title:str
    author:str
    genre: str
    price: float

    class Config:
        orm_mode=True


class AllBooks(BaseModel):
    books: list[BookModel] | None = None

    class Config:
        orm_mode = True