from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from .auth import get_current_user
from ..models import Todo
from ..dependencies import  db_dependency 


router = APIRouter(
    prefix="/admin", #imposta in automatico admin su tutto
    tags=['admin']
)

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Todo).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    todo_model=db.query(Todo)\
        .filter(Todo.id==todo_id)\
        .first()
        
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo non trovato')
    
    db.query(Todo)\
        .filter(Todo.id==todo_id)\
        .delete()
    
    db.commit()