from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email:EmailStr = Field(min_length=5, max_length=100)
    password:str = Field(min_length=5)
    full_name:str = Field(min_length=10, max_length=100)



class UserLogin(BaseModel):
    email:EmailStr = Field(min_length=5, max_length=100)
    password:str = Field(min_length=5)



class UserResponse(BaseModel):
    id:int
    email:EmailStr
    full_name:str
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True
    }


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "from_attributes": True
    }


