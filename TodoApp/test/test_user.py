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

def test_change_password_success(test_user):
    response = client.put("/user/change_password", 
                        json={"OldPassword":"admin",
                            "NewPassword":"admin1",
                            "NewPassword_confirm":"admin1"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password", 
                        json={"OldPassword":"admin2",
                            "NewPassword":"admin1",
                            "NewPassword_confirm":"admin1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error old password'}

def test_change_phone_number_success(test_user):
    response = client.put("/user/change_phone_number", 
                        json={"PhoneNumber":"39483949303"})
    assert response.status_code == status.HTTP_204_NO_CONTENT