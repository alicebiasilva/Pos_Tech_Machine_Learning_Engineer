from fastapi import APIRouter, HTTPException, Query
import pandas as pd

router = APIRouter()

# Carrega os dados do CSV ao iniciar a API
df_books = pd.read_csv("D:/FIAP/Engenharia de Machine Learning/Fase 1/Projeto1/tech_challenge/data/books.csv")  
df_books["id"] = df_books.index + 1


# Lista todos os livros
@router.get("/books", tags=["Livros"])
def get_books():
    return df_books.to_dict(orient="records")

# Detalhes de um livro pelo ID
@router.get("/books/{book_id}",tags=["Livros"])
def get_book(book_id: int):
    book = df_books[df_books["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book.to_dict(orient="records")[0]

# Busca livros por título e/ou categoria
@router.get("/books/search",tags=["Categorias"])
def search_books(title: str | None = Query(None), category: str | None = Query(None)):
    result = df_books
    if title:
        result = result[result["title"].str.contains(title, case=False, na=False)]
    if category:
        result = result[result["category"].str.contains(category, case=False, na=False)]
    return result.to_dict(orient="records")

# Lista todas as categorias
@router.get("/categories",tags=["Categorias"])
def get_categories():
    categories = df_books["category"].unique().tolist()
    return {"categories": categories}

# Health check
@router.get("/health",tags=["Saúde"])
def health():
    return {"status": "ok"}

#uvicorn tech_challenge.api.main:app --reload