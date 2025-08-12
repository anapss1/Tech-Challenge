from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from typing import List
from api.models import BookResponse
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

router = APIRouter(tags=["Books"])

df = pd.read_csv("data/livros.csv")
df["id"] = df.index
df["rating"] = df["rating"].astype(int)
df["preco"] = df["preco"].astype(float)

@router.get("/health")
async def status():
    """ Endpoint de verificação de saúde da API """
    return {"status": "ok", "livros_carregados": len(df)}


@router.get("/books")
async def books():
    """ Retorna todos os livros disponíveis na base de dados """
    return df.to_dict(orient="records")


@router.get("/books/categoria")
async def listar_categorias():
    """ Retorna todas as categorias disponíveis """
    return df["categoria"].unique().tolist()

@router.get("/books/search")
def buscar_livros(title: str = None, category: str = None):
    """Busca livros por título e/ou categoria"""
    resultado = df.copy()

    if title:
        resultado = resultado[resultado["titulo"].str.contains(title, case=False, na=False)]
    if category:
        resultado = resultado[resultado["categoria"].str.contains(category, case=False, na=False)]

    if resultado.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado com os critérios informados.")

    return resultado.to_dict(orient="records")



@router.get("/stats/overview")
def stats_gerais():
    """ Retorna estatísticas gerais dos livros """
    total_livros = len(df)
    preco_medio = round(df["preco"].mean(), 2)
    distribuicao_ratings = df["rating"].value_counts().sort_index().to_dict()
    
    return {
        "total_livros": total_livros,
        "preco_medio": preco_medio,
        "distribuicao_ratings": distribuicao_ratings
    }


@router.get("/stats/categories")
def stats_por_categoria():
    """ Retorna estatísticas por categoria """
    stats = df.groupby("categoria").agg(
        quantidade=("titulo", "count"),
        preco_medio=("preco", "mean"),
        preco_max=("preco", "max"),
        preco_min=("preco", "min")
    ).round(2).reset_index()

    return stats.to_dict(orient="records")

@router.get("/books/top-rated", response_model=List[BookResponse])
def livros_top_rating():
    """ Retorna os livros com a maior classificação """
    max_rating = df["rating"].max()
    top_livros = df[df["rating"] == max_rating]
    return top_livros.to_dict(orient="records")

@router.get("/books/price-range", response_model=List[BookResponse])
def livros_por_faixa_de_preco(min: float = Query(...), max: float = Query(...)):
    """ Retorna livros dentro de uma faixa de preço específica """
    if min > max:
        raise HTTPException(status_code=400, detail="O valor mínimo não pode ser maior que o máximo.")
    filtrado = df[(df["preco"] >= min) & (df["preco"] <= max)]
    return filtrado.to_dict(orient="records")




@router.get("/books/{id}")
async def livro_por_id(id: int):
    """ Retorna um livro específico pelo ID """
    if id not in df.index:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return df.loc[id].to_dict()
