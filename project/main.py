from app import app
from books.routes import books_router

app.include_router(books_router, prefix='/api/books', tags=['books'])
