from app import schemas
from jose import jwt
import pytest
from app.config import settings


# pytest -v -s tests/test_users.py

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'welcome home'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={'email': 'email@example.com', 'password': 'password123'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'email@example.com'
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']}
    )
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@email.com', 'password123', 403),
    ('email@example.com', 'wrong_password', 403),
    ('wrongemail@email.com', 'wrong_pasword', 403),
    (None, 'password123', 422),
    ('email@example.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials.'