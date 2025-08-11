from fastapi import FastAPI
from api.endpoints import router
from api.auth import router as auth_router

app = FastAPI(
    title="Books API",
    version="1.0",
    description="API pública de livros extraídos do books.toscrape.com"
)

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")