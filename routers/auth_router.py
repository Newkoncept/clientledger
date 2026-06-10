from fastapi import APIRouter
from starlette import status

from dependencies.db_dependency import db_dependency
from dependencies.user_dependency import user_dependency, token_dependency
from schemas.user_schema import UserCreate, UserResponse, UserLogin, UserLoginResponse
from services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(user:UserCreate, db: db_dependency):
    return auth_service.register_new_user(user, db)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login_user(db:db_dependency, user:UserLogin):
    return auth_service.login_user(db, user)


@router.post("/login/token", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login_token_validator(form_data: token_dependency, db: db_dependency):
    return auth_service.login_token_validator(form_data, db)


@router.get("/me", status_code=status.HTTP_200_OK, response_model = UserResponse)
def retrieve_user_details(db:db_dependency, user: user_dependency):
    return auth_service.retrieve_user_details(db, user)
    