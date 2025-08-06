from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="Books API",
    version="1.0",
    description="API pública de livros extraídos do books.toscrape.com"
)

app.include_router(router, prefix="/api/v1")