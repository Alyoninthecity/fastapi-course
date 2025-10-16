from .utils import *
from ..dependencies import get_db
from ..routers.auth import authUser, createAccessToken,get_current_user, SECRET_KEY, ALGORITHM
from fastapi import HTTPException
import pytest
from jose import jwt
from datetime import datetime, timedelta, timezone

app.dependency_overrides[get_db]=override_get_db

def test_auth_user(test_user):
    db = TestingSessionLocal()
    
    auth_User = authUser(test_user.username,'admin',db)
    assert auth_User is not None
    assert auth_User.username==test_user.username

    non_existent_user = authUser("RANDOM","NotCorrectPassword",db)
    assert non_existent_user is False
    
    wrong_password_user = authUser(test_user.username,'admin1',db)
    assert wrong_password_user is False

def test_create_access_token():
    username = 'testuser'
    user_id= 1
    user_role = 'user'
    expires = timedelta(days=1)

    token = createAccessToken(username, user_id,user_role,expires)
    
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],options={'verify_signature':False})
    assert decoded_token['sub']==username
    assert decoded_token['id']==user_id
    assert decoded_token['role']==user_role
    #Controllo se nel range la scadenza
    decoded_expires_time = datetime.fromtimestamp(decoded_token['exp'],tz=timezone.utc)
    assert decoded_expires_time < datetime.now(timezone.utc) + timedelta(days=1)
    assert decoded_expires_time > datetime.now(timezone.utc) + timedelta(days=1) - timedelta(seconds=5)

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'testuser','id':1,'role':'admin'}
    
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    
    user = await get_current_user(token=token)
    assert user == {'username':'testuser','id':1,'user_role':'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'sub':'testuser','role':'admin'}
    
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
    
        await get_current_user(token=token)  
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'