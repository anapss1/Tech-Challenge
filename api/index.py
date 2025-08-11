from fastapi import FastAPI
from api.endpoints import router
from api.auth import router as auth_router

app = FastAPI()

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
