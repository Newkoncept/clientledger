from fastapi import APIRouter
from starlette import status

from dependencies.db_dependency import db_dependency
from dependencies.user_dependency import user_dependency

from schemas.workspace_schema import WorkSpaceRequest, WorkSpaceResponse, WorkspaceFullResponse
from services import workspace_service

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"]
)


@router.post("", status_code=status.HTTP_200_OK, response_model=WorkspaceFullResponse)
def create_new_workspace(db: db_dependency, user: user_dependency, workspace:WorkSpaceRequest):
    return workspace_service.create_new_workspace(db, user, workspace)


@router.get("", response_model=list[WorkSpaceResponse], status_code=status.HTTP_200_OK)
def get_all_user_workspace(db: db_dependency, user:user_dependency):
    return workspace_service.get_all_user_workspace(db, user)
    

@router.get("/{id}", response_model=WorkSpaceResponse, status_code=status.HTTP_200_OK)
def get_workspace_by_id(db: db_dependency, user:user_dependency, id:int):
    return workspace_service.get_workspace_by_id(db, user, id)

