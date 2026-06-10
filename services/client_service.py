from fastapi import HTTPException
from starlette import status

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from models.Client import Client
from models.Workspace import Workspace

from schemas.client_schema import ClientCreateRequest, ClientUpdateRequest
from utilities.helpers import get_db_item_by_column



def create_client(db:db_dependency, user:user_dependency, client:ClientCreateRequest):
    workspace_exists = get_db_item_by_column(db, Workspace, "id", client.workspace_id)
    if not workspace_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace not found")
    
    clients_exists_in_workspace = db.query(Client).filter(Client.workspace_id == client.workspace_id).filter(Client.email == client.email).first()
    if clients_exists_in_workspace:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Client exists in this workspace")
    
    client_model = Client(**client.model_dump(exclude_unset=True))

    db.add(client_model)
    db.commit()
    db.refresh(client_model)

    return client_model


def update_client(db:db_dependency, user:user_dependency, client:ClientUpdateRequest, id:int):
    client_exists = get_db_item_by_column(db, Client, "id", id)
    if not client_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    updated_client_response = client.model_dump(exclude_unset=True)

    for key,value in updated_client_response.items():
        setattr(client_exists, key, value)

    db.add(client_exists)
    db.commit()


def delete_client(db:db_dependency, user:user_dependency, id:int):
    client = get_db_item_by_column(db, Client, "id", id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    db.delete(client)
    db.commit()


def get_client_info_with_workspace_id(db: db_dependency, user:user_dependency, id:int, name:str | None = None, email:str | None = None ):
    clients = db.query(Client).filter(Client.workspace_id == id)
    if name:
        clients = clients.filter(Client.name == name)
    if email:
        clients = clients.filter(Client.email == email)

    clients = clients.all()

    if not clients:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No result found")

    return clients


def get_client_info_with_id(db: db_dependency, user:user_dependency, id:int):
    client = get_db_item_by_column(db, Client, "id", id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    return client
