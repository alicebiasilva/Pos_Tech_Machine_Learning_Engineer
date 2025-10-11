import csv
import os

def save_books_csv(books: list[dict], filename: str = "public/data/books.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
    
    print(f"{len(books)} livros salvos em {filename}")
