from fastapi import status
from fastapi.testclient import TestClient

from ....service.core.security import hash_password
from ...conftest import TestSession
from ...db.factories.user import UserFactory
from ...db.factories.utils import fake


def test_success_register_user(
    client: TestClient,
    db_session: TestSession,
) -> None:
    password = fake.password()
    register_data = {
        "username": fake.name(),
        "password": password,
        "password_confirm": password,
    }
    response = client.post(f"/users/register", json=register_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_failed_register_user_missmatch_password(
    client: TestClient,
    db_session: TestSession,
) -> None:
    password = fake.password()
    register_data = {
        "username": fake.name(),
        "password": password,
        "password_confirm": fake.password(),
    }
    response = client.post(f"/users/register", json=register_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_failed_register_user_user_with_such_username_already_exists(
    client: TestClient,
    db_session: TestSession,
) -> None:
    password = fake.password()
    user = UserFactory(hashed_password=hash_password(password=password))
    register_data = {
        "username": user.username,
        "password": password,
        "password_confirm": password,
    }
    response = client.post(f"/users/register", json=register_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
