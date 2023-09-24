from fastapi.testclient import TestClient
import json

import sys
sys.path.append("app")

from main import app

client = TestClient(app)


def test_create_users():
    user_1 = {"name": "test1", "age": 20, "email": "email", "about_me": "string"}
    response = client.post("/users/create", json=user_1)
    assert response.status_code == 200
    assert response.json() == 1

    user_2 = {"name": "test2", "age": 10, "email": "email", "about_me": "string"}
    response = client.post("/users/create", json=user_2)
    assert response.status_code == 200
    assert response.json() == 2

def test_create_invalid_users():
    user = {"age": 20, "email": "email", "about_me": "string"}
    response = client.post("/users/create", json=user)
    assert response.status_code == 422

    user = {"name": "test2", "email": "email", "about_me": "string"}
    response = client.post("/users/create", json=user)
    assert response.status_code == 422

    user = {"name": "test2", "age": 20, "about_me": "string"}
    response = client.post("/users/create", json=user)
    assert response.status_code == 422
    
    user = {"name": "test1", "age": 20, "email": "email"}
    response = client.post("/users/create", json=user)
    assert response.status_code == 422


def test_get_users():
    user_1 = {"name": "test1", "age": 20, "email": "email", "about_me": "string"}
    user_2 = {"name": "test2", "age": 10, "email": "email", "about_me": "string"}
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [user_1, user_2]


def test_get_user():
    user_1 = {"name": "test1", "age": 20, "email": "email", "about_me": "string"}
    user_2 = {"name": "test2", "age": 10, "email": "email", "about_me": "string"}

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user_1

    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json() == user_2

    response = client.get("/users/3")
    assert response.status_code == 404

def test_edit_user():
    user = {"name": "Test 3", "age": 56, "email": "None", "about_me": "Что-то есть, а нет, показалось)"}

    response = client.put("/users/edit", json={"user": user, "user_id": 1})
    assert response.status_code == 200

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user


def test_edit_invalid_user():
    invalid_user = {"name": "", "age": 0, "email": ""}
    user = {"name": "Test 3", "age": 56, "email": "None", "about_me": "Что-то есть, а нет, показалось)"}

    response = client.put("/users/edit", json={"user": invalid_user, "user_id": 1})
    assert response.status_code == 422

    response = client.put("/users/edit", json={"user": user, "user_id": 1000})
    assert response.status_code == 404

def test_create_friendship():
    response = client.post("/friendship/create", json={"user_id": 1, "friend_id": 2})
    assert response.status_code == 200
    assert response.json() == {"status": "successfully"}

    response = client.get("/friendship/1")
    assert response.status_code == 200
    assert response.json() == [2]

    response = client.get("/friendship/2")
    assert response.status_code == 200
    assert response.json() == [1]

def test_create_invalid_friendship():
    response = client.post("/friendship/create", json={"user_id": 1, "friend_id": 100})
    assert response.status_code == 404
    
    response = client.post("/friendship/create", json={"user_id": 1000, "friend_id": 2})
    assert response.status_code == 404
    
    response = client.post("/friendship/create", json={"user_id": 1})
    assert response.status_code == 422
    
    response = client.post("/friendship/create", json={"friend_id": 2})
    assert response.status_code == 422
