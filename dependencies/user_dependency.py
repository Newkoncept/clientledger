from utilities.user_utilities import get_current_user
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm


user_dependency = Annotated[dict, Depends(get_current_user)]

token_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

