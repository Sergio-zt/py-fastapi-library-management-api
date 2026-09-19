from pydentic import BaseModel

from typing import List, Optional


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None

class BookList(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int
    books: List[BookList] = []

    class Config:
        from_attributes = True