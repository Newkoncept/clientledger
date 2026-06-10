from fastapi import APIRouter
from starlette import status

from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.workspacemember_schema import (
    WorkspaceMemberResponse, WorkspaceMemberRequest, 
    WorkspaceMemberDeleteRequest, WorkspaceMemberUpdateRequest
)
from services import workspacemember_service

router = APIRouter(
    prefix="/workspace-members",
    tags=["workspace member"]
)


@router.post("", response_model=WorkspaceMemberResponse, status_code=status.HTTP_201_CREATED)
def add_new_workspace_member(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberRequest):
    return workspacemember_service.add_new_workspace_member(db, user, workspacemember)
    

@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_member_role(db:db_dependency, user:user_dependency, workspacemember: WorkspaceMemberUpdateRequest, id:int):
    workspacemember_service.update_member_role(db, user, workspacemember, id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def remove_workspace_member_by_user_id(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberDeleteRequest):
    workspacemember_service.remove_workspace_member_by_user_id(db, user, workspacemember)
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_workspace_member(db: db_dependency, user: user_dependency, id:int):
    workspacemember_service.remove_workspace_member(db, user, id)

