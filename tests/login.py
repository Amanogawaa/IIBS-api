import pytest
from api.crud.user import login_user
from types import SimpleNamespace
from fastapi import HTTPException
from api.utils import hash_password

# python


class DummyUser:
    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

class DummyDBSession:
    def __init__(self, user=None):
        self._user = user

    def query(self, model):
        class Query:
            def __init__(self, user):
                self._user = user
            def filter(self, cond):
                class First:
                    def __init__(self, user):
                        self._user = user
                    def first(self):
                        return self._user
                return First(self._user)
        return Query(self._user)

@pytest.fixture
def valid_user():
    # hashed password for 'password123'
    return DummyUser(
        id=1,
        email="test@example.com",
        username="testuser",
        password=hash_password("password123")
    )

def test_login_success(valid_user):
    db = DummyDBSession(user=valid_user)
    req = SimpleNamespace(email="test@example.com", password="password123")
    token = login_user(req, db)
    assert hasattr(token, "access_token")
    assert hasattr(token, "refresh_token")

def test_login_invalid_email(valid_user):
    db = DummyDBSession(user=None)
    req = SimpleNamespace(email="wrong@example.com", password="password123")
    with pytest.raises(HTTPException) as exc:
        login_user(req, db)
    assert exc.value.status_code == 400
    assert "Invalid Email" in str(exc.value.detail)

def test_login_invalid_password(valid_user):
    db = DummyDBSession(user=valid_user)
    req = SimpleNamespace(email="test@example.com", password="wrongpass")
    with pytest.raises(HTTPException) as exc:
        login_user(req, db)
    assert exc.value.status_code == 400
    assert "Invalid Password" in str(exc.value.detail)

def test_login_empty_email(valid_user):
    db = DummyDBSession(user=None)
    req = SimpleNamespace(email="", password="password123")
    with pytest.raises(HTTPException) as exc:
        login_user(req, db)
    assert exc.value.status_code == 400

def test_login_empty_password(valid_user):
    db = DummyDBSession(user=valid_user)
    req = SimpleNamespace(email="test@example.com", password="")
    with pytest.raises(HTTPException) as exc:
        login_user(req, db)
    assert exc.value.status_code == 400