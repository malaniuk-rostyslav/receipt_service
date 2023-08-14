from fastapi import FastAPI

from .controllers.api import api_router
from .core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)
