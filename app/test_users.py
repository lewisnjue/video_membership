
import pytest 
from app import db  
from app.users.models import User

@pytest.fixture(scope='module')
def setup():
    session =db.get_session()
    yield session
    q = User.objects.filter(email="test@gmail.com")
    if q.count() !=0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test@gmail.com",password="tesing123")



def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@gmail.com",password="tesing123")

def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@gmail.com",password="tesing123")

def test_valid_password(setup):
    q = User.objects.filter(email='test@gmail.com')
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('tesing123') == True



