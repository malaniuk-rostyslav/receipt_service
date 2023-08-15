from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from .controllers.api import api_router
from .core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)  # noqa
app.include_router(api_router)
# Set all CORS enabled origins
add_pagination(app)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],  # noqa
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
