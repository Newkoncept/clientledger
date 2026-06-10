from fastapi import HTTPException
from starlette import status
from dependencies.user_dependency import user_dependency
from dependencies.db_dependency import db_dependency

from schemas.workspacemember_schema import WorkspaceMemberRequest, WorkspaceMemberDeleteRequest, WorkspaceMemberUpdateRequest
from utilities.helpers import get_db_item_by_column
from models.WorkspaceMember import WorkspaceMember
from models.User import User
from models.Workspace import Workspace


def add_new_workspace_member(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberRequest):
    user_exists_in_db = get_db_item_by_column(db, User, "id", workspacemember.user_id)
    if not user_exists_in_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    workspace_exists = get_db_item_by_column(db, Workspace, "id", workspacemember.workspace_id)
    if not workspace_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "workspace not found")
    
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == workspacemember.user_id).filter(WorkspaceMember.workspace_id == workspacemember.workspace_id).first()
    if user_exists_in_workspace:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User exists in the workspace already")
    
    workspacemember_model = WorkspaceMember(**workspacemember.model_dump())

    db.add(workspacemember_model)
    db.commit()
    db.refresh(workspacemember_model)

    return workspacemember_model


def update_member_role(db:db_dependency, user:user_dependency, workspacemember: WorkspaceMemberUpdateRequest, id:int):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    for key, value in workspacemember.model_dump(exclude_unset=True).items():
        setattr(user_exists_in_workspace, key, value)

    db.add(user_exists_in_workspace)
    db.commit()


def remove_workspace_member_by_user_id(db: db_dependency, user: user_dependency, workspacemember: WorkspaceMemberDeleteRequest):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == workspacemember.user_id).filter(WorkspaceMember.workspace_id == workspacemember.workspace_id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    db.delete(user_exists_in_workspace)
    db.commit()


def remove_workspace_member(db: db_dependency, user: user_dependency, id:int):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    db.delete(user_exists_in_workspace)
    db.commit()
