from fastapi import HTTPException
from starlette import status

from dependencies.db_dependency import db_dependency
from dependencies.user_dependency import user_dependency
from models import Workspace, WorkspaceMember
from schemas.workspace_schema import WorkSpaceRequest


def create_new_workspace(db: db_dependency, user: user_dependency, workspace:WorkSpaceRequest):
    try: 
        workspace_value = Workspace(**workspace.model_dump())
        workspace_value.owner_id = user.get("user_id")
        db.add(workspace_value)
        db.flush()

        workspacemember_model = WorkspaceMember(workspace_id = workspace_value.id, user_id = workspace_value.owner_id, role = "owner")
        db.add(workspacemember_model)
        
        db.commit()
        db.refresh(workspace_value)
        db.refresh(workspacemember_model)

        return {
            "workspace": workspace_value,
            "workspace_member": workspacemember_model
        }
    except Exception:
        db.rollback()
        raise


def get_all_user_workspace(db: db_dependency, user:user_dependency):
    workspaces = db.query(Workspace).filter(Workspace.owner_id == user.get("user_id")).all()
    if not workspaces:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No workspace found")
    
    return workspaces

    
def get_workspace_by_id(db: db_dependency, user:user_dependency, id:int):
    workspace = db.query(Workspace).filter(Workspace.id == id).first()

    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No workspace found")
    
    if workspace.owner_id != user.get("user_id"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized access")
    return workspace


