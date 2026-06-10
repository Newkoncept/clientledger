from fastapi import HTTPException
from starlette import status
from datetime import timedelta

from dependencies.db_dependency import db_dependency
from dependencies.user_dependency import user_dependency, token_dependency

from models import User
from schemas.user_schema import UserCreate, UserLogin

from utilities.helpers import get_db_item_by_column, login_token_generator
from utilities.user_utilities import authenticate_user, create_access_token, hash_password


def register_new_user(user:UserCreate, db: db_dependency):
    if get_db_item_by_column(db, User, "email", user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email exists already")
    
    user_model = User(**user.model_dump())
    user_model.password = hash_password(user.password)

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


def login_user(db:db_dependency, user:UserLogin):
    user_value = authenticate_user(user.email, user.password, db)
    return login_token_generator(user_value.id, timedelta(minutes = 20))


def login_token_validator(form_data: token_dependency, db: db_dependency):
    user_value = authenticate_user(form_data.username, form_data.password, db)
    return login_token_generator(user_value.id, timedelta(minutes = 20))


def retrieve_user_details(db:db_dependency, user: user_dependency):
    user = db.query(User).filter(User.id == user.get("user_id")).first()
    return user
    