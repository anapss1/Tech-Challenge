from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi import Request

router = APIRouter(tags=["Auth"])

class UserLogin(BaseModel):

    """Modelo de dados recebidos para o login"""
    username: str
    password: str

class Settings(BaseModel):
    """Configuracao da chave secreta"""
    authjwt_secret_key: str = "chave-secreta-segura"

@AuthJWT.load_config
def get_config():
    return Settings()

FAKE_USER = {
    "username": "admin",
    "password": "1234"
}

@router.post("/auth/login")
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    """Rota de Login"""
    if user.username != FAKE_USER["username"] or user.password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalido")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/auth/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    """Renova o token"""
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": access_token}
