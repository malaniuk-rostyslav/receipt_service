from typing import Dict, Generator, Tuple

import pytest
from fastapi.testclient import TestClient

from backend.db.models import User

from ...service.core.security import create_access_token, hash_password
from ...service.core.settings import settings
from ...service.main import app
from ..db.factories.user import UserFactory
from ..db.factories.utils import fake


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_and_headers(client: TestClient) -> Tuple[User, Dict[str, str]]:
    password = fake.password()
    user = UserFactory.create(hashed_password=hash_password(password=password))
    access_token = create_access_token(
        subject=user.username, exp_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return user, headers
