from factory.alchemy import SQLAlchemyModelFactory

from server.backend.tests.conftest import TestSession

factory_session = TestSession()


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = factory_session
        sqlalchemy_session_persistence = "commit"
