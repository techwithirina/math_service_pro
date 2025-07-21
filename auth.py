# auth.py
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

security = HTTPBearer()

# Load tokens from env
VALID_TOKENS = {
    os.getenv("USER_TOKEN"): "user",
    os.getenv("ADMIN_TOKEN"): "admin"
}


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return VALID_TOKENS[token]
