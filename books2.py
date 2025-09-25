from typing import Optional
from fastapi import FastAPI,Body, HTTPException, Path,Query
from pydantic import BaseModel, Field
from datetime import datetime
from starlette import status
'''
GET status_code=status.HTTP_200_OK
POST status_code=status.HTTP_201_CREATED
PUT status_code=status.HTTP_200_OK oppure status_code=status.HTTP_204_NO_CONTENT
'''

app=FastAPI()


def get_current_year():
    return datetime.now().year
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int
    
    def __init__(self,id,title,author,description,rating,publish_date=get_current_year()):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.publish_date=publish_date

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="Id non necessario in create", default=None) #Mettere sempre None se voglio aggiungere Field
    title: str = Field(min_length=3,max_length=100)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rating: int = Field(gt=0,lt=6,description="Rating da 1 a 5") #Da 1 a 5
    publish_date : int = Field(ge=0,le=get_current_year(), description="Anno di pubblicazione")
    
    #VALORI DI DEFAULT PER IL JSON TRAMITE /DOCS
    model_config= {
        "json_schema_extra":{
            "example" : {
                "title":"Nuovo libro",
                "author":"Autore",
                "description":"Descrizione libro",
                "rating":5,
                "publish_date":get_current_year()
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

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.post("/create-book/", status_code=status.HTTP_201_CREATED)
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

@app.get("/books/{book_id}/", status_code=status.HTTP_200_OK)
async def read_book_id(book_id: int= Path(gt=0)):
    for book in BOOKS:
        if book_id == book.id:
            return book
    raise HTTPException(status_code=404,detail="Libro non trovato")

@app.get("/books/sort_by_rating/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int=Query(gt=0,lt=6)):
    book_ok=[]
    for book in BOOKS:
        if book_rating == book.rating:
            book_ok.append(book)
    if not book_ok:
        raise HTTPException(status_code=404,detail="Libro non trovato")
    else:
        return book_ok
    

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    books_updated=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            books_updated=True
    if not books_updated:
        raise HTTPException(status_code=404,detail="Libro non trovato")

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int=Path(gt=0)):
    for i in BOOKS:
        if i.id==book_id:
            BOOKS.remove(i)
            return i
    raise HTTPException(status_code=404,detail="Libro non trovato")

@app.get("/books/sort_by_publish_date", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(publish_date:int=Query(gt=1990)):
    book_to_return=[]
    for book in BOOKS:
        if book.publish_date==publish_date:
            book_to_return.append(book)
    return book_to_return