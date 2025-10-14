from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from .auth import get_current_user
from ..models import User
from ..dependencies import  db_dependency 
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user", #imposta in automatico admin su tutto
    tags=['user']
)

user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #Per Hashing

class ChangePasswordRequest(BaseModel):
    OldPassword : str
    NewPassword : str = Field(min_length=6)
    NewPassword_confirm : str = Field(min_length=6)
    
class ChangePhoneNumberRequest(BaseModel):
    PhoneNumber : str = Field (min_length=10, max_length=15)

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user_logged:user_dependency,db:db_dependency):
    if user_logged is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    return db.query(User).filter(User.id == user_logged.get('id')).first()

@router.put('/change_password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user_logged:user_dependency,db:db_dependency,change_password:ChangePasswordRequest):
    if user_logged is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    user_model=db.query(User).filter(User.id==user_logged.get('id')).first()
    
    if not bcrypt_context.verify(change_password.OldPassword ,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='Error old password')
    
    if (change_password.NewPassword != change_password.NewPassword_confirm):
        raise HTTPException(status_code=401,detail='Error new password not equal to new password confirm')
    
    user_model.hashed_password = bcrypt_context.hash(change_password.NewPassword)
    
    db.add(user_model)
    db.commit()



@router.put('/change_phone_number',status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user_logged:user_dependency,db:db_dependency,change_phone_number:ChangePhoneNumberRequest):
    if user_logged is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    user_model=db.query(User).filter(User.id==user_logged.get('id')).first()
    
    user_model.phone_number = change_phone_number.PhoneNumber
    
    db.add(user_model)
    db.commit()
