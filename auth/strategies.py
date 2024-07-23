from fastapi_users.authentication import JWTStrategy
from core.config import setting

SECRET = "SECRET"


# Strategy JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(
#         secret=setting.auth_jwt.private_key_path.read_text(),
#         lifetime_seconds=3600,
#         algorithm=setting.auth_jwt.algorithm,
#         public_key=setting.auth_jwt.public_key_path.read_text(),
#     )
