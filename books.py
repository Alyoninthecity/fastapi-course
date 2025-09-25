from fastapi import Body, FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Book(BaseModel):
    title: str
    author: str
    category: str

class BookTitle(BaseModel):
    title: str

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'},
    {'title': 'Title One', 'author': 'Author Two', 'category': 'science'},
]



@app.get("/api-endpoint")
async def first_api():
    return {"message": "Ciao Massimo!"}

#PRIMA LE COSE STATICHE POI LE DINAMICHE
@app.get("/books/")
async def read_all_books():
    return BOOKS

'''
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {"dynamic_param": dynamic_param}
'''

# Path Parameters
@app.get("/books/titolo/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book['title'].lower() == book_title.lower():
            return book
        
@app.get("/books/id/{numero_libro}")
async def read_all_books(numero_libro: int):
    try: 
        return BOOKS[numero_libro - 1]
    except IndexError:
        return {"error": "Book not found"}

# Query Parameters
@app.get("/books/category/")
async def read_category_by_query(category_name: str):
    books_in_category = []
    for book in BOOKS:
        if book['category'].lower() == category_name.lower():
            books_in_category.append(book)
    return books_in_category

#Path + Query Parameters
#localhost:8000/books/Author%20Two/?category=math
@app.get("/books/{book_author}/")
async def read_author_by_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book['author'].lower() == book_author.lower() and book['category'].lower() == category.lower():
            books_to_return.append(book)
    return books_to_return
'''
#POST Request BASIC 
@app.post("/books/create_book/")
async def create_book(new_book= Body()): 
    BOOKS.append(new_book)
'''
#LE GET NON POSSONO AVERE I BODY

#POST Request con Struttura
@app.post("/books/create_book/")
async def create_book(new_book: Book = Body(...)): #I 3 puntini indicano che è obbligatorio il parametro
    BOOKS.append(new_book)
    
#PUT Request Method
@app.put("/books/{book_title}/title/")
async def update_book_title(book_title:str, new_title: BookTitle=Body(...)):
    update_books=[]
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            book["title"]=new_title.title
            update_books.append(book)
            
    if not update_books:
        raise HTTPException(status_code=404,detail="Libro non trovato")
    return {"message":"Titoli aggiornato per", "books":update_books}

#DELETE Request Method
@app.delete("/book/delete_book/{book_title}")
async def delete_book(book_title: str):
    deleted_books=[]
    for book in BOOKS:
        if book["title"]==book_title:
            deleted_books.append(book)
            BOOKS.remove(book)
    if not deleted_books:
        raise HTTPException(status_code=404,detail="Libro non trovato")
    return {"message":"Libri rimossi", "books":deleted_books}
