from pydantic import AnyUrl


class PostgresDsn(AnyUrl):
    allowed_schemes = {"postgres", "postgresql", "postgresql+asyncpg"}
    user_required = True
