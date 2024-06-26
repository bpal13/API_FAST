import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{settings.db_password}@{settings.db_host}:5432/fastapi_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # run code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # run code after test finishes


@pytest.fixture 
def test_user(client):
    user_data = {'email': 'email1@example.com', 'password': 'password12345'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture 
def test_user2(client):
    user_data = {'email': 'email@example.com', 'password': 'password123'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            'title': 'first title',
            'content': 'first content',
            'owner_id': test_user['id']
        },
        {
            'title': 'second title',
            'content': 'second content',
            'owner_id': test_user['id']            
        },
        {
            'title': '3rd title',
            'content': '3rd content',
            'owner_id': test_user['id']
        },
        {
            'title': '3rd title',
            'content': '3rd content',
            'owner_id': test_user2['id']
        }]
    
    def create_post_model(post):
        return models.Posts(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Posts).all()
    return posts