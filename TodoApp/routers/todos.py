from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Path
from starlette import status
from models import Todo
from dependencies import  db_dependency 


router = APIRouter()


class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int = Field(gt=0,lt=6)
    complete : bool


@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Todo).all()



@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id==todo_id).first() #Siccome l'id è univoco e per salvare prestazioni prendo appena lo trova con first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo non trovato')

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request:TodoRequest):
    
    todo_model= Todo(**todo_request.model_dump())
    
    db.add(todo_model)
    db.commit()



@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_request:TodoRequest, todo_id:int= Path(gt=0)):
    todo_model=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo non trovato')
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    
    
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo non trovato')
    db.query(Todo).filter(Todo.id==todo_id).delete()
    
    db.commit()