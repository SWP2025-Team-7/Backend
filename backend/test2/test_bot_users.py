from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
import pytest

from backend.db.repositories.bot_users import BotUsersRepository
from backend.api.dependencies.database import get_repository
from backend.db.server import app

def test_register_bot_user(client):
    response = client.post("/students/register", json={
        "new_bot_user": {
            "user_id": 1,
            "login_date": "2025-02-01",
            "login_time": "15:34:00",
            "last_used_date": "2025-02-01",
            "last_used_time": "15:34:00"
        }
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1


def test_register_bot_user_missing_field(client):
    response = client.post("/students/register", json={
        "new_bot_user": {
            # "user_id" is missing
            "login_date": "2025-07-06",
            "login_time": "14:00:00",
            "last_used_date": "2025-07-06",
            "last_used_time": "14:00:00"
        }
    })

    assert response.status_code == 422

def test_register_bot_user_invalid_date_format(client):
    response = client.post("/students/register", json={
        "new_bot_user": {
            "user_id": 456,
            "login_date": "invalid-date",  # wrong format
            "login_time": "14:00:00",
            "last_used_date": "2025-07-06",
            "last_used_time": "14:00:00"
        }
    })

    assert response.status_code == 422
