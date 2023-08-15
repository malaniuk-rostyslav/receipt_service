from passlib.context import CryptContext

pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_contex.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_contex.verify(password, hash)
