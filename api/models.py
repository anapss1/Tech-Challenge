from pydantic import BaseModel

class Book(BaseModel):
    id: int
    titulo: str
    preco: str
    rating: str
    disponibilidade: str
    categoria: str
    imagem: str
