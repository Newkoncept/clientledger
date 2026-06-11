from sqlalchemy.orm import Session

from schemas.workspacemember_schema import WorkSpaceMemberRole
from fastapi import HTTPException
from starlette import status

from models.WorkspaceMember import WorkspaceMember

ADMIN = [WorkSpaceMemberRole.OWNER ,WorkSpaceMemberRole.ADMIN]
STAFF = [WorkSpaceMemberRole.OWNER ,WorkSpaceMemberRole.ADMIN, WorkSpaceMemberRole.STAFF]


def role_checker(category:list, user_role:WorkSpaceMemberRole | str):
    if user_role not in category:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access control Error: Your access clearance is not permitted, contact your manager")
    


def user_permitted(db:Session, user:dict, workspace_id:int, allowed_roles: list):
    user_workspace_detail:WorkspaceMember = db.query(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).filter(WorkspaceMember.user_id == user.get("user_id")).first()
    if not user_workspace_detail:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission Error: You are not allowed to access this workspace")

    role_checker(allowed_roles, user_workspace_detail.role)
    return user_workspace_detail


def prevent_self_detail_update(user_detail:WorkspaceMember, user_id:int, action:str):
    message = ""
    if action == "update":
        message = "You can't update your role"
    else:
        message = "You can't delete your account"

    if user_detail.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Permission Error: {message}')


def owner_only(user_detail:WorkspaceMember, role_to_be_updated:str):
    if role_to_be_updated in ADMIN and user_detail.role != WorkSpaceMemberRole.OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission Error: Only the owner can make CREATE/UPDATE/DELETE for this user role")
    