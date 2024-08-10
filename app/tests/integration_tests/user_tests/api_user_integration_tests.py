from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("mymail@mail.ru", "mypass", 200),
    ("mymail@mail.ru", "mypass1", 409),
    ("mymailru", "mypass1", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@example.com", "test", 200)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code
