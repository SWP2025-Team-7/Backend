from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
import pytest

from backend.db.repositories.users import UsersRepository
from backend.api.dependencies.database import get_repository
from backend.db.server import app

def test_create_user(client):
    response = client.post("/users/", json={
        "user_id": 1,
        "alias": "test",
        "mail": "test@example.com",
        "name": "John",
        "surname": "Doe",
        "patronymic": "Testovich",
        "phone_number": 1234567890,           # int, а не строка
        "citizens": "Country",
        "duty_to_work": "yes",                 # ok, enum есть "yes"
        "duty_status": "working",              # поменяли с "active" на "working"
        "grant_amount": 1000,
        "duty_period": 6,                      # int, а не "6 months"
        "company": "TestCorp",
        "resume_path": "/path/to/resume",
        "position": "Developer",
        "start_date": "2023-01-01",
        "end_date": "2023-06-01",
        "salary": 50000,
        "working_reference_path": "/ref/path",
        "ndfl1_path": "/ndfl/1",
        "ndfl2_path": "/ndfl/2",
        "ndfl3_path": "/ndfl/3",
        "ndfl4_path": "/ndfl/4"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["alias"] == "test"

def test_create_user_missing_field(client):
    response = client.post("/users/", json={})  # пустой запрос
    assert response.status_code == 422  # ошибка валидации

def test_get_nonexistent_user():
    app.dependency_overrides[get_repository(UsersRepository)] = lambda: mock_repo
    mock_repo = MagicMock()
    mock_repo.get_user_by_id = AsyncMock(return_value=None)

    client = TestClient(app)
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_update_user(client):
    # Сначала создаём пользователя
    response = client.post("/users/", json={
        "user_id": 2,
        "alias": "old_alias",
        "mail": "update@example.com",
        "name": "Update",
        "surname": "User",
        "patronymic": "Updatevich",
        "phone_number": 1234567890,
        "citizens": "Country",
        "duty_to_work": "yes",
        "duty_status": "working",
        "grant_amount": 1000,
        "duty_period": 6,
        "company": "OldCorp",
        "resume_path": "/old/resume",
        "position": "Engineer",
        "start_date": "2023-01-01",
        "end_date": "2023-06-01",
        "salary": 45000,
        "working_reference_path": "/ref/old",
        "ndfl1_path": "/ndfl/a",
        "ndfl2_path": "/ndfl/b",
        "ndfl3_path": "/ndfl/c",
        "ndfl4_path": "/ndfl/d"
    })
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    # Обновим alias и компанию
    update_response = client.patch(f"/users/{user_id}", json={
        "alias": "new_alias",
        "company": "NewCorp"
    })
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["alias"] == "new_alias"
    assert updated["company"] == "NewCorp"

def test_delete_user(client):
    # Сначала создаём пользователя
    response = client.post("/users/", json={
        "user_id": 3,
        "alias": "delete_me",
        "mail": "delete@example.com",
        "name": "Delete",
        "surname": "User",
        "patronymic": "Deletevich",
        "phone_number": 1234567890,
        "citizens": "Country",
        "duty_to_work": "yes",
        "duty_status": "working",
        "grant_amount": 1000,
        "duty_period": 6,
        "company": "DeleteCorp",
        "resume_path": "/delete/resume",
        "position": "QA",
        "start_date": "2023-01-01",
        "end_date": "2023-06-01",
        "salary": 47000,
        "working_reference_path": "/ref/del",
        "ndfl1_path": "/ndfl/1a",
        "ndfl2_path": "/ndfl/2b",
        "ndfl3_path": "/ndfl/3c",
        "ndfl4_path": "/ndfl/4d"
    })
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    # Удаление
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    # Проверим, что пользователь удалён
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
