from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.AuthorResponse])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)

@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse)
def create_book_for_author(
    author_id: int, 
    book: schemas.BookCreate, 
    db: Session = Depends(get_db)
):
    db_author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
        
    return crud.create_book_for_author(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=List[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)
