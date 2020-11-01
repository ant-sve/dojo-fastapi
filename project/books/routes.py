from typing import List, Dict, Optional, Any

from fastapi import APIRouter

from drivers import MongoDriver
from .dao import BookDAO
from .schemas import (
    DBBookSchema,
    BaseBookSchema,
    ResponseCreateSchema,
    ResponseUpdateSchema,
    ResponseRemoveSchema,
)

books_router = APIRouter()

_dao = BookDAO(driver=MongoDriver, collection_name='myCollection')


@books_router.get('/all', response_model=List[BaseBookSchema], status_code=200)
async def get_all_books() -> List[Dict[str, Any]]:
    books = _dao.get_all_books()

    return [book async for book in books if book is not None]


@books_router.get(
    '/',
    response_model=Optional[BaseBookSchema],
    status_code=200,
)
async def get_book(title: str) -> DBBookSchema:
    book = await _dao.get_book_by_title(title)

    return book


@books_router.post('/', response_model=ResponseCreateSchema, status_code=200)
async def create_one(book: BaseBookSchema) -> Dict[str, Any]:
    inserted = await _dao.insert_one_book(book)

    response = {'inserted': inserted}

    return response


@books_router.put('/', response_model=ResponseUpdateSchema, status_code=200)
async def update_one(title: str, book: BaseBookSchema) -> Dict[str, Any]:
    modified_count = await _dao.replace_one_book_by_title(title, book)

    response = {'modified': modified_count}

    return response


@books_router.delete('/', response_model=ResponseRemoveSchema, status_code=200)
async def remove_one(title: str) -> Dict[str, Any]:
    removed_count = await _dao.remove_one_book_by_title(title)

    response = {'removed': removed_count}

    return response
