import pytest
'''
Validate Integers "=="
Validate Instances with "isInstance" or "not isInstante"
Validate Booleans with "is True"
Validate Types with "is str"
Validate Greater Than & Less Than "<" or ">"

'''
def test_equal_or_not_equal():
    assert 3==3
    assert 3!=1


def test_is_instance():
    assert isinstance("Test",str)
    
def test_boolean():
    validate = True
    assert validate is True
    assert ("Home"=="Home") is True

def test_type():
    assert type("Hello" is str)
    assert type("World" is not int)

def test_greater_and_less_than():
    assert 3<7
    assert 10>8

def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)
    
class Student:
    def __init__(self, first_name:str,last_name:str,major:str,year:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.year=year

@pytest.fixture
def default_employee():
    return Student('John','Doe','Computer Science',3)

def test_person_initialization(default_employee):
    assert default_employee.first_name=='John','First name should be John'
    assert default_employee.last_name=='Doe','Last name should be Doe'
    assert default_employee.major=='Computer Science'
    assert default_employee.year==3
    