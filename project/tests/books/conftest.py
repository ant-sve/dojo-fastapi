import unittest.mock as mock

import pytest

from fastapi.testclient import TestClient

from books.routes import books_router, ROUTE_PREFIX, TAGS
from books.schemas import DBBookSchema
from .factories import DBBookFactory


@pytest.fixture
def book_routes(test_app):
    test_app.include_router(books_router, prefix=ROUTE_PREFIX, tags=TAGS)

    return test_app


@pytest.fixture
def books_test_client(book_routes):
    return TestClient(book_routes)


@pytest.fixture
def books_dao_mock():
    dao_patch = mock.patch('books.routes._dao')

    yield dao_patch.start()

    dao_patch.stop()


@pytest.fixture
def books_dao_async_mock():
    dao_patch = mock.patch('books.routes._dao', new=mock.AsyncMock)

    yield dao_patch.start()

    dao_patch.stop()


@pytest.fixture
def db_book():
    factory_object = DBBookFactory.build()

    return DBBookSchema(**factory_object.dict())


@pytest.fixture
def db_book_and_external_json(db_book):
    external_json = {k: v for k, v in db_book.dict().items() if k != 'pk'}

    return db_book, external_json
