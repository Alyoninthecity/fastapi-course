from fastapi import  APIRouter
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from dependencies import  db_dependency
from starlette import status

'''
Hashing delle password
    pip install passlib 
    pip install bcrypt==4.0.1
'''
router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #Per Hashing

class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str
    role : str

@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                    create_user_request:CreateUserRequest):
    
    create_user_model=User(      #User(**create_user_request.model_dump())Non funziona perché da una parte ho password e da una parte hashed_password
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    ) 
    db.add(create_user_model)
    db.commit()
    