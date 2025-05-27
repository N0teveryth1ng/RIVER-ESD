# backend/auth_routes.py

from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from jose import jwt
from dotenv import load_dotenv
import os
import time

load_dotenv()
router = APIRouter()

# Dummy users (you can later link this to DB)
fake_users = {
    "user_001": "password123",
    "S1": "sellerpass1",
    "S2": "sellerpass2",
    "S3": "sellerpass3"
}

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 3600

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Accept any username and password - no checks
    payload = {
        "sub": username,
        "exp": time.time() + TOKEN_EXPIRE_SECONDS
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return JSONResponse({"access_token": token, "token_type": "bearer"})



from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


__all__ = ["router", "verify_user"]
