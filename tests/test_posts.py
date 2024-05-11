import pytest
from typing import List
from app import schemas
from tests.conftest import client


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')


    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert posts_list[0].Posts.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')

    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get('/posts/88888')

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')

    post = schemas.PostOut(**res.json())

    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ('new title', 'some new content', True),
    ('pizza time', 'some content', False),
    ('check this out', 'big content', True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


@pytest.mark.parametrize("title, content", [
    ('new title', 'some new content'),
    ('pizza time', 'some content'),
    ('check this out', 'big content'),
])
def test_create_post_default_published_true(authorized_client, test_user, title, content):
    res = authorized_client.post('/posts/', json={'title': title, 'content': content})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_create_post_unauthorized_client(client):
    res = client.post('/posts/', json={'title': 'some title', 'content': 'some content'})

    assert res.status_code == 401


def test_unauthorized_client_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')

    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete('/posts/99999')

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')

    assert res.status_code == 401


def test_update_post(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }

    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**res.json())

    assert  res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_posts, test_user2):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }

    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)

    assert  res.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = client.put(f'/posts/{test_posts[3].id}', json=data)

    assert res.status_code == 401


def test_update_post_non_existent(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = authorized_client.put('/posts/9999', json=data)

    assert res.status_code == 404