import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users/", json={
        "user_id": 1,
        "alias": "test",
        "mail": "test@example.com",
        "name": "John",
        "surname": "Doe",
        "patronymic": "Testovich",
        "phone_number": "1234567890",
        "citizens": "Country",
        "duty_to_work": "yes",
        "duty_status": "active",
        "grant_amount": 1000,
        "duty_period": "6 months",
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
