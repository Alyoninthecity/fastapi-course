from ..main import app
from ..dependencies import get_db
from ..routers.auth import get_current_user

from fastapi import status
from .utils import *
import pytest
from ..models import Todo

#Override Dependency Injection for TESTING MOC
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== [{'title':"Learn to Code",
                                "description":"Need to learn okkk??",
                                "priority":5,
                                "complete":False,
                                "owner":1,
                                'id':1}
                            ]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== {'title':"Learn to Code",
                                "description":"Need to learn okkk??",
                                "priority":5,
                                "complete":False,
                                "owner":1,
                                'id':1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code== status.HTTP_404_NOT_FOUND
    assert response.json()== {'detail':'Todo non trovato'}
    
def test_create_todo(test_todo):
    request_data = {
                    'title':"Learn to Code Create",
                    "description":"Need to learn okkk??",
                    "priority":5,
                    "complete":False,
                    }
    response = client.post('/todo/',json=request_data)
    assert response.status_code== status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data = {
                    "title":"Change the tile",       
                    "description":"Need to learn okkk??",
                    "priority":4,
                    "complete":False,
                    }
    
    response = client.put('/todo/1',json=request_data)
    assert response.status_code== status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
    
def test_update_todo_not_found(test_todo):
    request_data = {
                    "title":"Change the tile",       
                    "description":"Need to learn okkk??",
                    "priority":4,
                    "complete":False,
                    }
    
    response = client.put('/todo/999',json=request_data)
    assert response.status_code== status.HTTP_404_NOT_FOUND
    assert response.json()== {'detail':'Todo non trovato'}

def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code== status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==1).first()
    assert model is None
    
def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code== status.HTTP_404_NOT_FOUND
    assert response.json()== {'detail':'Todo non trovato'}
