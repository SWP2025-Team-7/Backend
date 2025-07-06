import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock, MagicMock
from backend.routes.user import router as user_router
from backend.routes.students import router as students_router

@pytest.fixture
def client():
    test_app = FastAPI()
    test_app.include_router(user_router)
    test_app.include_router(students_router)

    # Создаем мок базы
    mock_db = MagicMock()
    mock_db.connect = AsyncMock()
    mock_db.disconnect = AsyncMock()

    # ВАЖНО: fetch_one тоже асинхронный метод — заменим на AsyncMock
    mock_db.fetch_one = AsyncMock(return_value={
    "id": 1,
    "user_id": 1,
    "alias": "test",
    "mail": "test@example.com",
    "name": "John",
    "surname": "Doe",
    "patronymic": "Testovich",
    "phone_number": 1234567890,
    "citizens": "Country",
    "duty_to_work": "yes",
    "duty_status": "working",
    "grant_amount": 1000,
    "duty_period": 6,
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
    "ndfl4_path": "/ndfl/4",
    })


    test_app.state._db = mock_db

    with patch("backend.db.tasks.connect_to_db", new=AsyncMock()), \
         patch("backend.db.tasks.close_db_connection", new=AsyncMock()):
        with TestClient(test_app) as c:
            yield c
