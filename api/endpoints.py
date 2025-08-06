from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from api.models import Book


"""
Endpoints Obrigatórios da API
Endpoints Core
• GET /api/v1/books: Lista todos os livros disponíveis na base de dados.
• GET /api/v1/books/{id}: Retorna detalhes completos de um livro
específico pelo ID.
• GET /api/v1/books/search?title={title}&category={category}: Busca
livros por título e/ou categoria.
• GET /api/v1/categories: Lista todas as categorias de livros disponíveis.
• GET /api/v1/health: Verifica status da API e conectividade com os
dados.
 
"""

router = APIRouter()

df = pd.read_csv("data/livros.csv")
df["id"] = df.index

@router.get("/health")
def status():
    return {"status": "ok", "livros_carregados": len(df)}

@router.get("/books")
def books():
    return df.to_dict(orient="records")

@router.get("/books/{id}", response_model=Book)
def livro_por_id(id: int):
    if id not in df.index:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return df.loc[id].to_dict()

@router.get("/categoria", response_model=list[str])
def listar_categorias():
    return df["categoria"].unique().tolist()