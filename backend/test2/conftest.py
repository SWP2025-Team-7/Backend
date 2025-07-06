import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock, MagicMock
from backend.routes.students import router as students_router

@pytest.fixture
def client():
    test_app = FastAPI()
    test_app.include_router(students_router)

    # Создаем мок базы
    mock_db = MagicMock()
    mock_db.connect = AsyncMock()
    mock_db.disconnect = AsyncMock()

    # ВАЖНО: fetch_one тоже асинхронный метод — заменим на AsyncMock
    mock_db.fetch_one = AsyncMock(return_value={
        "id": 1,
        "user_id": 1,
        "login_date": "2025-02-01",
        "login_time": "15:34:00",
        "last_used_date": "2025-02-01",
        "last_used_time": "15:34:00"
    })


    test_app.state._db = mock_db

    with patch("backend.db.tasks.connect_to_db", new=AsyncMock()), \
         patch("backend.db.tasks.close_db_connection", new=AsyncMock()):
        with TestClient(test_app) as c:
            yield c
