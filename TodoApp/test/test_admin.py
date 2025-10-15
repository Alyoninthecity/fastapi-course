from .utils import *
from ..routers.admin import get_current_user
from ..dependencies import get_db
from fastapi import status

#Override Dependency Injection for TESTING MOC
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()== [{'title':"Learn to Code",
                                "description":"Need to learn okkk??",
                                "priority":5,
                                "complete":False,
                                "owner":1,
                                'id':1}
                            ]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    assert db.query(Todo).filter(Todo.id == 1).first() is None

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo non trovato'}