from .utils import *
from ..routers.admin import get_current_user
from ..dependencies import get_db
from fastapi import status
from passlib.context import CryptContext

#Override Dependency Injection for TESTING MOC
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #Per Hashing

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id']==1
    assert response.json()['username']=='admin'
    assert response.json()['email']=='email@'
    assert response.json()['first_name']=='admin'
    assert response.json()['last_name']=='admin'
    assert bcrypt_context.verify('admin',response.json()['hashed_password'])
    assert response.json()['is_active']==True
    assert response.json()['role']=='admin'
    assert response.json()['phone_number']=='312313'