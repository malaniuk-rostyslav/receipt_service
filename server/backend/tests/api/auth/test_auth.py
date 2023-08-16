from fastapi import status
from fastapi.testclient import TestClient

from ....service.core.security import hash_password
from ...conftest import TestSession
from ...db.factories.user import UserFactory
from ...db.factories.utils import fake


def test_success_obtain_access_token(
    client: TestClient,
    db_session: TestSession,
) -> None:
    password = fake.password()
    user = UserFactory(hashed_password=hash_password(password=password))
    login_data = {
        "username": user.username,
        "password": password,
    }
    response = client.post(f"/auth/access-token", data=login_data)
    assert response.status_code == status.HTTP_200_OK


def test_failed_obtain_access_token_wrong_credentials(
    client: TestClient,
    db_session: TestSession,
) -> None:
    password = fake.password()
    user = UserFactory(hashed_password=hash_password(password=password))
    login_data = {
        "username": user.username,
        "password": fake.password(),
    }
    response = client.post(f"/auth/access-token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
