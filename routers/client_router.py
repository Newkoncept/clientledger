from fastapi import APIRouter
from starlette import status

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.client_schema import ClientCreateRequest, ClientResponse, ClientUpdateRequest
from services import client_service

router = APIRouter(
    prefix = "/clients",
    tags = ["clients"]
)


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(db:db_dependency, user:user_dependency, client:ClientCreateRequest):
    return client_service.create_client(db, user, client)



@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_client(db:db_dependency, user:user_dependency, client:ClientUpdateRequest, id:int):
    client_service.update_client(db, user, client, id)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(db:db_dependency, user:user_dependency, id:int):
    client_service.delete_client(db, user, id)



@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[ClientResponse])
def get_client_info_with_workspace_id(db: db_dependency, user:user_dependency, id:int, name:str | None = None, email:str | None = None ):
    return client_service.get_client_info_with_workspace_id(db, user, id, name, email)



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ClientResponse)
def get_client_info_with_id(db: db_dependency, user:user_dependency, id:int):
    return client_service.get_client_info_with_id(db, user, id)