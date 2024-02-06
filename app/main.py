from fastapi import FastAPI, Depends, Response, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .exception import UnicornException, TestException
from typing import Optional
from sqlalchemy.sql import desc, asc

Base.metadata.create_all(bind=engine)

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request:Request, exc:UnicornException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Book with id = {exc.id} was not found!"}
    )

@app.exception_handler(TestException)
async def test_exception_handler(request:Request, exc:TestException):
    return JSONResponse(
        status_code=400,
        content={"id":exc.id,"message":exc.msg}
    )

@app.post("/api/books/", response_model=schemas.BookModel)
def create_book(payload:schemas.BookModel,response:Response, db:Session = Depends(get_db)):
    book = crud.create_book(payload=payload, db=db)
    if book:
        response.status_code = status.HTTP_201_CREATED
    return book


@app.put("/api/books/{id}")
def update_book(id:int, payload:schemas.UpdateBook, db:Session=Depends(get_db)):
    return crud.update_book(id=id, payload=payload, db=db)

@app.get("/api/books/{id}", response_model=schemas.BookModel)
def get_book(id:int, db:Session=Depends(get_db)):
    return crud.get_book(id=id, db=db)

# @app.get("/api/books/")
# def get_book_by_search(request:Request, title:str|None=None, author:str|None = None, genre:str|None = None):
#     dct = dict(request.query_params)
#     print(dct)

@app.get("/api/books/", response_model=schemas.AllBooks)
def get_books(req:Request, title:str|None=None, author:str|None=None, genre:str|None=None,sort:str|float|None=None,order:str|None=None, db:Session = Depends(get_db) ):

    params = dict(req.query_params)
    
    if not bool(params):
        return {"books": crud.get_books(db)}

    if 'title' in params:
        if 'sort' in params:
            if params['sort'] == 'title':
                if 'order' in params :
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.title)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(desc(models.Books.title)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.title)).all()}
            elif params['sort'] == 'author':
                if 'order' in params :
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.author)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(desc(models.Books.author)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.author)).all()}
            elif params['sort'] == 'genre':
                if 'order' in params :
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.genre)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(desc(models.Books.genre)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.genre)).all()}
            elif params['sort'] == 'price':
                if 'order' in params :
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.price)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(desc(models.Books.price)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.price)).all()}
        else:
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).filter(params['title'] == models.Books.title).order_by(asc(models.Books.id))}
                else:
                    return {"books": db.query(models.Books).filter(params['title'] == models.Books.title).order_by(desc(models.Books.id))}
            else:
                return {"books": db.query(models.Books).filter(params['title']==models.Books.title).order_by(asc(models.Books.id))}
            
    elif 'author' in params:
        if 'sort' in params:
            if params['sort'] == 'title':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.title)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(desc(models.Books.title)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.title)).all()}
            elif params['sort'] == 'author':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.author)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(desc(models.Books.author)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.author)).all()}
            elif params['sort'] == 'genre':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.genre)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(desc(models.Books.genre)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.genre)).all()}
            elif params['sort'] == 'price':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.price)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(desc(models.Books.price)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.price)).all()}
        else:
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).filter(params['author'] == models.Books.author).order_by(asc(models.Books.id))}
                else:
                    return {"books": db.query(models.Books).filter(params['author'] == models.Books.author).order_by(desc(models.Books.id))}
            else:
                return {"books": db.query(models.Books).filter(params['author']==models.Books.author).order_by(asc(models.Books.id))}
    elif 'genre' in params :
        if 'sort' in params :
            if params['sort'] == 'title':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.title)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(desc(models.Books.title)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.title)).all()}
            elif params['sort'] == 'author':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.author)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(desc(models.Books.author)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.author)).all()}
            elif params['sort'] == 'genre':
                if'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.genre)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(desc(models.Books.genre)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.genre)).all()}
            elif params['sort'] == 'price':
                if 'order' in params:
                    if params['order'] == 'ASC':
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.price)).all()}
                    else:
                        return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(desc(models.Books.price)).all()}
                else:
                    return {"books": db.query(models.Books).filter(params['genre']==models.Books.genre).order_by(asc(models.Books.price)).all()}
        else:
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).filter(params.genre == models.Books.genre).order_by(asc(models.Books.id))}
                else:
                    return {"books": db.query(models.Books).filter(params['genre'] == models.Books.genre).order_by(desc(models.Books.id))}
            else:
                return {"books": db.query(models.Books).filter(params.genre==models.Books.genre).order_by(asc(models.Books.id))}
    elif 'sort' in params:
        if params['sort'] == 'title':
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).order_by(asc(models.Books.title)).all()}
                else:
                    return {"books": db.query(models.Books).order_by(desc(models.Books.title)).all()}
            else:
                return {"books": db.query(models.Books).order_by(asc(models.Books.title)).all()}
        elif params['sort'] == 'author':
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).order_by(asc(models.Books.author)).all()}
                else:
                    return {"books": db.query(models.Books).order_by(desc(models.Books.author)).all()}
            else:
                return {"books": db.query(models.Books).order_by(asc(models.Books.author)).all()}
        elif params['sort'] == 'genre':
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).order_by(asc(models.Books.genre)).all()}
                else:
                    return {"books": db.query(models.Books).order_by(desc(models.Books.genre)).all()}
            else:
                return {"books": db.query(models.Books).order_by(asc(models.Books.genre)).all()}
        elif params['sort'] == 'price':
            if 'order' in params:
                if params['order'] == 'ASC':
                    return {"books": db.query(models.Books).order_by(asc(models.Books.price)).all()}
                else:
                    return {"books": db.query(models.Books).order_by(desc(models.Books.price)).all()}
            else:
                return {"books": db.query(models.Books).order_by(asc(models.Books.price)).all()}
    elif 'order' in params:
        if params['order'] == 'ASC':
            return {"books": db.query(models.Books).order_by(asc(models.Books.id)).all()}
        else:
            return {"books": db.query(models.Books).order_by(desc(models.Books.id)).all()}