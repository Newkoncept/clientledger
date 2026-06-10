from datetime import timedelta

from fastapi import APIRouter, HTTPException
from starlette import status

from models import User
from dependencies.db_dependency import db_dependency
from dependencies.user_dependency import user_dependency, token_dependency
from schemas.user_schema import UserCreate, UserResponse, UserLogin, UserLoginResponse
from utilities.helpers import get_db_item_by_column
from utilities.user_utilities import authenticate_user, create_access_token, hash_password


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(user:UserCreate, db: db_dependency):
    if get_db_item_by_column(db, User, "email", user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email exists already")
    
    user_model = User(**user.model_dump())
    user_model.password = hash_password(user.password)

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login_user(db:db_dependency, user:UserLogin):
    user_value = authenticate_user(user.email, user.password, db)

    token = create_access_token(user_value.id, timedelta(minutes = 20))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login/token", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login_token_validator(form_data: token_dependency, db: db_dependency):
    user_value = authenticate_user(form_data.username, form_data.password, db)

    token = create_access_token(user_value.id, timedelta(minutes = 20))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", status_code=status.HTTP_200_OK, response_model = UserResponse)
def retrieve_user_details(db:db_dependency, user: user_dependency):

    user = db.query(User).filter(User.id == user.get("user_id")).first()
    return user
    