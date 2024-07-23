from fastapi_users.authentication import BearerTransport

# Transport Bearer
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
