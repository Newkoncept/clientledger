from fastapi import HTTPException, APIRouter
from starlette import status
from datetime import date

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from models.Project import Project
from models.Workspace import Workspace
from models.Client import Client

from schemas.project_schema import (ProjectCreateRequest, ProjectUpdateRequest, 
                                    ProjectResponse, ProjectFullSummaryResponse
                                )
from utilities.helpers import get_db_item_by_column


router = APIRouter(
    prefix = "/projects",
    tags = ["projects"]
)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
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


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(db:db_dependency, user:user_dependency, project:ProjectUpdateRequest, id:int):
    project_exists = get_db_item_by_column(db, Project, "id", id)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Project not found")
       
    project_model = project.model_dump(exclude_unset=True)
    for key, value in project_model.items():
        setattr(project_exists, key, value)

    db.add(project_exists)
    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(db:db_dependency, user:user_dependency, id:int):
    project_exists = get_db_item_by_column(db, Project, "id", id)
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Project not found")
    
    db.delete(project_exists)
    db.commit()


@router.get("/{id}/project", status_code=status.HTTP_200_OK, response_model=ProjectResponse)
def get_project_by_project_id(db:db_dependency, user:user_dependency, id:int):
    project_exists= get_db_item_by_column(db, Project, "id", id)

    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return project_exists


@router.get("/{id}/summary", status_code=status.HTTP_200_OK, response_model=ProjectFullSummaryResponse)
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


@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[ProjectResponse])
def get_project_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, name:str | None = None, project_status:str | None= None,
                                start_date:date | None= None, due_date:date | None= None
                            ):
    project_exists= db.query(Project).filter(Project.workspace_id == id)
    if not project_exists.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if name:
        project_exists = project_exists.filter(Project.name == name)
    if project_status:
        project_exists = project_exists.filter(Project.status == project_status)
    if start_date:
        project_exists = project_exists.filter(Project.start_date == start_date)
    if due_date:
        project_exists = project_exists.filter(Project.due_date == due_date)
    
    project_exists = project_exists.all()
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")    

    return project_exists

   
@router.get("/client/{id}", status_code=status.HTTP_200_OK, response_model=list[ProjectResponse])
def get_project_by_client_id(db:db_dependency, user:user_dependency, 
                            id:int, name:str | None = None, project_status:str | None= None,
                            start_date:date | None= None, due_date:date | None= None
                        ):
    project_exists= db.query(Project).filter(Project.client_id == id)
    
    if not project_exists.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if name:
        project_exists = project_exists.filter(Project.name == name)
    if project_status:
        project_exists = project_exists.filter(Project.status == project_status)
    if start_date:
        project_exists = project_exists.filter(Project.start_date == start_date)
    if due_date:
        project_exists = project_exists.filter(Project.due_date == due_date)
    
    
    
    project_exists = project_exists.all()
    if not project_exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Project not found")    

    return project_exists

