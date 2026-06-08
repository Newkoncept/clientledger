from fastapi import FastAPI
from starlette import status
from routers import auth_router, workspace_router, workspacemember_router

app = FastAPI()






@app.get('/health', status_code = status.HTTP_200_OK)
def health():
    return "Server running successfully"


app.include_router(auth_router.router)
app.include_router(workspace_router.router)
app.include_router(workspacemember_router.router)