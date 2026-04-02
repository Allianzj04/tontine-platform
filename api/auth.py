from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(username: str):
  exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  payload = {"sub": username, "exp": exp}
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
  try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    payload = decoded["sub"]
    return payload
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")