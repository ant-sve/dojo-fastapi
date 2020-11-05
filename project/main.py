from app import app
from books.routes import books_router, ROUTE_PREFIX, TAGS

app.include_router(books_router, prefix=ROUTE_PREFIX, tags=TAGS)
# TODO: Add util to auto import routes


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8008)
