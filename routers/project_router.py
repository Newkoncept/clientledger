from fastapi import APIRouter
from starlette import status
from datetime import date

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency


from schemas.project_schema import (ProjectCreateRequest, ProjectUpdateRequest, 
                                    ProjectResponse, ProjectFullSummaryResponse
                                )

from services import project_service


router = APIRouter(
    prefix = "/projects",
    tags = ["projects"]
)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(db:db_dependency, user:user_dependency, project:ProjectCreateRequest):
    return project_service.create_project(db, user, project)


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project(db:db_dependency, user:user_dependency, project:ProjectUpdateRequest, id:int):
    project_service.update_project(db, user, project, id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(db:db_dependency, user:user_dependency, id:int):
    project_service.delete_project(db, user, id)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProjectResponse)
def get_project_by_project_id(db:db_dependency, user:user_dependency, id:int):
    return project_service.get_project_by_project_id(db, user, id)


@router.get("/{id}/summary", status_code=status.HTTP_200_OK, response_model=ProjectFullSummaryResponse)
def get_project_full_summary_by_project_id(db:db_dependency, user:user_dependency, id:int):
    return project_service.get_project_full_summary_by_project_id(db, user, id)


@router.get("/workspace/{id}", status_code=status.HTTP_200_OK, response_model=list[ProjectResponse])
def get_project_by_workspace_id(db:db_dependency, user:user_dependency, 
                                id:int, name:str | None = None, project_status:str | None= None,
                                start_date:date | None= None, due_date:date | None= None):
    return project_service.get_project_by_workspace_id(db, user, id, name, project_status, start_date, due_date)

   
@router.get("/client/{id}", status_code=status.HTTP_200_OK, response_model=list[ProjectResponse])
def get_project_by_client_id(db:db_dependency, user:user_dependency, 
                            id:int, name:str | None = None, project_status:str | None= None,
                            start_date:date | None= None, due_date:date | None= None):
    return project_service.get_project_by_client_id(db, user, id, name, project_status, start_date, due_date)

