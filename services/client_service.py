from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from models.Client import Client
from models.Workspace import Workspace

from schemas.client_schema import ClientCreateRequest, ClientUpdateRequest
from dependencies.permission import user_permitted
from utilities.helpers import get_db_item_by_column



def create_client(db:Session, user:dict, client:ClientCreateRequest, role_allowed:list):
    user_permitted(db, user, client.workspace_id, role_allowed)
    
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


def update_client(db:Session, user:dict, client:ClientUpdateRequest, id:int, role_allowed:list):
    client_exists = get_db_item_by_column(db, Client, "id", id)
    if not client_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    user_permitted(db, user, client_exists.workspace_id, role_allowed)

    if client.email:
        if client.email == client_exists.email:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "A new email address is needed")
        
        email_exists_in_workspace = db.query(Client).filter(Client.workspace_id == client_exists.workspace_id).filter(Client.email == client.email).first()
        if email_exists_in_workspace:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email exists in this workspace")
    


    updated_client_response = client.model_dump(exclude_unset=True)

    for key,value in updated_client_response.items():
        setattr(client_exists, key, value)

    db.add(client_exists)
    db.commit()


def delete_client(db:Session, user:dict, id:int, role_allowed:list):
    client = get_db_item_by_column(db, Client, "id", id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    user_permitted(db, user, client.workspace_id, role_allowed)

    db.delete(client)
    db.commit()


def get_client_info_with_workspace_id(db: Session, user:dict, id:int, name:str | None = None, email:str | None = None , role_allowed:list | None = None):

    user_permitted(db, user, id, role_allowed)

    clients = db.query(Client).filter(Client.workspace_id == id)
    if name:
        clients = clients.filter(Client.name == name)
    if email:
        clients = clients.filter(Client.email == email)

    clients = clients.all()

    if not clients:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No result found")

    return clients


def get_client_info_with_id(db: Session, user:dict, id:int, role_allowed:list):
    client = get_db_item_by_column(db, Client, "id", id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    
    user_permitted(db, user, client.workspace_id, role_allowed)    
    return client

