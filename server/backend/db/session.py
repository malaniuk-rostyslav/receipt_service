from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..service.core.settings import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
