
import pytest 

from app.users.models import User



def test_create_user():
    User.create_user(email="test@gmail.com",password="tesing123")
    

def test_equal():
    assert 1 ==1

def test_invalid_assert():
    with pytest.raises(AssertionError):
        assert True == False