from fastapi import Response
import bcrypt
import jwt

from core.config import setting, COOKIE_NAME


def create_hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    print("pwd_bytes", pwd_bytes)
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def encode_jwt(
    payload: dict,
    private_key: str = setting.auth_jwt.private_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = setting.auth_jwt.public_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def set_cookie(
    response: Response,
    token: str,
) -> None:
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True)
