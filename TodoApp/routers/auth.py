from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import  APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from ..models import User
from passlib.context import CryptContext
from ..dependencies import  db_dependency
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from fastapi.templating import Jinja2Templates

import os


'''
Hashing delle password
    pip install passlib 
    pip install bcrypt==4.0.1
'''
router = APIRouter(
    prefix="/auth", #imposta in automatico auth su tutto
    tags=['auth']
)

#SECRET_KEY='' #es. openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM='HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #Per Hashing

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') #URL che il client manda per la verifica

class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str
    role : str
    phone_number : str

class Token(BaseModel):
    access_token:str
    token_type:str

templates = Jinja2Templates(directory="TodoApp/templates")

### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html",{"request":request})

### Endpoints ###
def authUser(username:str,password:str,db):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def createAccessToken(username:str, user_id:int,role:str, expires_delta:timedelta):
    encode = {'sub':username,'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        user_role:str=payload.get('role')
        
        if username is None or user_id is None or user_role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
        return {'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                    create_user_request:CreateUserRequest):
    
    create_user_model=User(      #User(**create_user_request.model_dump())   Non funziona perché da una parte ho password e da una parte hashed_password
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    ) 
    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                db:db_dependency):
    user = authUser(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
    
    token= createAccessToken(user.username, user.id, user.role,timedelta(minutes=15))
    return {'access_token':token,'token_type':'bearer'}