from fastapi import APIRouter, HTTPException
from schemas.workspacemember_schema import (
    WorkspaceMemberResponse, WorkspaceMemberRequest, 
    WorkspaceMemberDeleteRequest, WorkspaceMemberUpdateRequest
)
from starlette import status
from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency
from utilities.helpers import item_exists_in_db
from models.WorkspaceMember import WorkspaceMember
from models.User import User
from models.Workspace import Workspace

router = APIRouter(
    prefix="/workspacemember",
    tags=["workspace member"]
)


@router.post("", response_model=WorkspaceMemberResponse, status_code=status.HTTP_201_CREATED)
def add_new_workspace_member(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberRequest):
    user_exists_in_db = item_exists_in_db(db, User, workspacemember.user_id, "id")
    if not user_exists_in_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    workspace_exists = item_exists_in_db(db, Workspace, workspacemember.workspace_id, "id")
    if not workspace_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Worskpace not found")
    
    user_exists_in_worskpace = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == workspacemember.user_id).filter(WorkspaceMember.workspace_id == workspacemember.workspace_id).first()
    if user_exists_in_worskpace:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User exists in the workspace already")
    
    workspacemember_model = WorkspaceMember(**workspacemember.model_dump())

    db.add(workspacemember_model)
    db.commit()
    db.refresh(workspacemember_model)

    return workspacemember_model


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_member_role(db:db_dependency, user:user_dependency, workspacemember: WorkspaceMemberUpdateRequest, id:int):
    user_exists_in_worskpace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_worskpace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    for key, value in workspacemember:
        setattr(user_exists_in_worskpace, key, value)

    db.add(user_exists_in_worskpace)
    db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def remove_workspace_member_by_user_id(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberDeleteRequest):
    user_exists_in_worskpace = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == workspacemember.user_id).filter(WorkspaceMember.workspace_id == workspacemember.workspace_id).first()
    if not user_exists_in_worskpace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    db.delete(user_exists_in_worskpace)
    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_workspace_member(db: db_dependency, user: user_dependency, id:int):
    user_exists_in_worskpace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_worskpace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    db.delete(user_exists_in_worskpace)
    db.commit()



