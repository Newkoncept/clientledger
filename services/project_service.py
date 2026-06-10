from fastapi import HTTPException
from starlette import status
from datetime import date

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from models.Project import Project
from models.Workspace import Workspace
from models.Client import Client

from schemas.project_schema import ProjectCreateRequest, ProjectUpdateRequest
from utilities.helpers import get_db_item_by_column, project_search_filter



def create_project(db:db_dependency, user:user_dependency, project:ProjectCreateRequest):
    workspace_exists = get_db_item_by_column(db, Workspace, "id", project.workspace_id)
    if not workspace_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Workspace not found")
    
    client_exists = get_db_item_by_column(db, Client, "id", project.client_id)
    if not client_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Client not found")

    if client_exists.workspace_id != project.workspace_id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Client not in this workspace")
    
    
    project_model = Project(**project.model_dump())

    db.add(project_model)
    db.commit()
    db.refresh(project_model)

    return project_model


def update_project(db:db_dependency, user:user_dependency, project:ProjectUpdateRequest, id:int):
    project_exists = get_db_item_by_column(db, Project, "id", id)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Project not found")
       
    project_model = project.model_dump(exclude_unset=True)
    for key, value in project_model.items():
        setattr(project_exists, key, value)

    db.add(project_exists)
    db.commit()


def delete_project(db:db_dependency, user:user_dependency, id:int):
    project_exists = get_db_item_by_column(db, Project, "id", id)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Project not found")
    
    db.delete(project_exists)
    db.commit()


def get_project_by_project_id(db:db_dependency, user:user_dependency, id:int):
    project_exists= get_db_item_by_column(db, Project, "id", id)

    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return project_exists


def get_project_full_summary_by_project_id(db:db_dependency, user:user_dependency, id:int):
    project_exists= get_db_item_by_column(db, Project, "id", id)

    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")

    workspace_detail = get_db_item_by_column(db, Workspace, "id", project_exists.workspace_id)
    client_detail = get_db_item_by_column(db, Client, "id", project_exists.client_id)

    return {
        "id" : project_exists.id,
        "name" : project_exists.name,
        "description" : project_exists.description,
        "status" : project_exists.status,
        "start_date" : project_exists.start_date,
        "due_date" : project_exists.due_date,
        "workspace" : workspace_detail,
        "client" : client_detail,
        "created_at" : project_exists.created_at,
        "updated_at" : project_exists.updated_at
    }


def get_project_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, name:str | None = None, project_status:str | None= None,
                                start_date:date | None= None, due_date:date | None= None
                            ):
    project_exists = project_search_filter(db, Project, "workspace_id", id, name, project_status, start_date, due_date)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")    

    return project_exists

   
def get_project_by_client_id(db:db_dependency, user:user_dependency, 
                            id:int, name:str | None = None, project_status:str | None= None,
                            start_date:date | None= None, due_date:date | None= None
                        ):
    project_exists = project_search_filter(db, Project, "client_id", id, name, project_status, start_date, due_date)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")    

    return project_exists

