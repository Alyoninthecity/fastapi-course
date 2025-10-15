from .utils import *
from ..dependencies import get_db
from ..routers.auth import authUser
from fastapi import status
from passlib.context import CryptContext

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
