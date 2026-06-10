from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("Missing SECRET_KEY or ALGORITHM environment variable")


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)



def create_access_token(user_id:int, expires_delta:timedelta):
    encode = {
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id:int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
        return {
            "user_id": user_id
        }
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")


def authenticate_user(email:str, password:str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email or password is incorrect")
    return user


