import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from ..db.base import Base
from ..service.core.deps import get_db
from ..service.main import app


def get_sync_test_db_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("TEST_POSTGRES_DB", "test_receipt_service_database")
    return f"postgresql://{user}:{password}@{server}/{db}"


TEST_DB_URI = get_sync_test_db_url()
test_engine_ = create_engine(TEST_DB_URI)
TestSession = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=test_engine_)
)


@pytest.fixture(scope="function")
def setup_db():
    if not database_exists(TEST_DB_URI):
        create_database(TEST_DB_URI)
    yield
    for table in reversed(Base.metadata.sorted_tables):
        TestSession.execute(table.delete())
    TestSession.commit()


@pytest.fixture(scope="function", autouse=True)
def setup_test_db(setup_db):
    with test_engine_.begin():
        Base.metadata.create_all(test_engine_)
        yield


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """yields a SQLAlchemy connection which is rollback after the test"""

    def override_get_db():
        with TestSession() as test_session:
            yield test_session

    app.dependency_overrides[get_db] = override_get_db
