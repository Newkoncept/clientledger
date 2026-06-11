from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from models.WorkspaceMember import WorkspaceMember
from models.User import User
from models.Workspace import Workspace

from schemas.workspacemember_schema import (WorkspaceMemberRequest, 
                                            WorkspaceMemberDeleteRequest, WorkspaceMemberUpdateRequest
                                        )
from dependencies.permission import user_permitted, prevent_self_detail_update, owner_only
from utilities.helpers import get_db_item_by_column


def add_new_workspace_member(db: Session, user: dict, workspacemember: WorkspaceMemberRequest, role_allowed:list):
    admin_detail = user_permitted(db, user, workspacemember.workspace_id, role_allowed)
    owner_only(admin_detail, workspacemember.role)

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


def update_member_role(db:Session, user:dict, workspacemember: WorkspaceMemberUpdateRequest, id:int, role_allowed:list):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    admin_detail = user_permitted(db, user, user_exists_in_workspace.workspace_id, role_allowed)
    prevent_self_detail_update(admin_detail, user_exists_in_workspace.user_id, "update")
    owner_only(admin_detail, workspacemember.role)
    owner_only(admin_detail, user_exists_in_workspace.role)

    for key, value in workspacemember.model_dump(exclude_unset=True).items():
        setattr(user_exists_in_workspace, key, value)

    db.add(user_exists_in_workspace)
    db.commit()


def remove_workspace_member_by_user_id(db: Session, user: dict, workspacemember: WorkspaceMemberDeleteRequest, role_allowed:list):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == workspacemember.user_id).filter(WorkspaceMember.workspace_id == workspacemember.workspace_id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")
    
    admin_detail = user_permitted(db, user, user_exists_in_workspace.workspace_id, role_allowed)
    prevent_self_detail_update(admin_detail, user_exists_in_workspace.user_id, "delete")
    owner_only(admin_detail, user_exists_in_workspace.role)

    db.delete(user_exists_in_workspace)
    db.commit()


def remove_workspace_member(db: Session, user: dict, id:int, role_allowed:list):
    user_exists_in_workspace = db.query(WorkspaceMember).filter(WorkspaceMember.id == id).first()
    if not user_exists_in_workspace:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace Member not found")

    admin_detail = user_permitted(db, user, user_exists_in_workspace.workspace_id, role_allowed)
    prevent_self_detail_update(admin_detail, user_exists_in_workspace.user_id, "delete")
    owner_only(admin_detail, user_exists_in_workspace.role)
    
    db.delete(user_exists_in_workspace)
    db.commit()

