from typing import Optional
from fastapi import FastAPI,Body, HTTPException
from pydantic import BaseModel, Field

app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="Id non necessario in create", default=None) #Mettere sempre None se voglio aggiungere Field
    title: str = Field(min_length=3,max_length=100)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rating: int = Field(gt=0,lt=6) #Da 1 a 5
    
    #VALORI DI DEFAULT PER IL JSON TRAMITE /DOCS
    model_config= {
        "json_schema_extra":{
            "example" : {
                "title":"Nuovo libro",
                "author":"Autore",
                "description":"Descrizione libro",
                "rating":5
            }
        }
    }


BOOKS=[
    Book(1,"Computer Science","codingwithjomama","Nice book",5),
    Book(2,"Computer Science1","codingwithjomama","Nice booko1",5),
    Book(3,"Computer Science2","codingwithjomama","Nice booko2",5),
    Book(4,"Computer Science3","codingwithjomama","Nice booko3",5),
    Book(5,"Computer Science4","codingwithjomama","Nice booko4",5),
    Book(6,"Computer Science5","codingwithjomama","Nice booko5",5),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book/")
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.model_dump()) #Altrimenti sto passando un BookRequest dentro ai miei libri se non creo un oggetto Book
    print(type(new_book))
    BOOKS.append(find_last_book_id(new_book))
    
def find_last_book_id(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id = 1
    return book

@app.get("/books/{book_id}/")
async def reab_book_id(book_id: int):
    for book in BOOKS:
        if book_id == book.id:
            return book
    raise HTTPException(status_code=404,detail="Libro non trovato")

@app.get("/books/sort_by_rating/")
async def reab_book_by_rating(book_rating: int):
    book_ok=[]
    for book in BOOKS:
        if book_rating == book.rating:
            book_ok.append(book)
    if not book_ok:
        raise HTTPException(status_code=404,detail="Libro non trovato")
    else:
        return book_ok
    
