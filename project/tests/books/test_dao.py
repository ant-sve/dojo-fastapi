import unittest.mock as mock

import pytest

from books.dao import BookDAO
from books.schemas import DBBookSchema


class TestBookDAO:

    @pytest.mark.asyncio
    async def test_get_book_by_title__valid_title__return_entity(self):
        driver_mock = mock.MagicMock
        get_mock = mock.AsyncMock(name='get_mock')
        get_mock.return_value = {
            '_id': 0,
            'author': 'test_author',
            'title': 'test_title',
        }

        test_book_dao = BookDAO(driver=driver_mock)
        test_book_dao.driver.get = get_mock

        test_result = await test_book_dao.get_book_by_title(title='title')

        assert isinstance(test_result, DBBookSchema)

    @pytest.mark.asyncio
    async def test_get_book_by_title__invalid_title__return_none(self):
        driver_mock = mock.MagicMock
        get_mock = mock.AsyncMock(name='get_mock')
        get_mock.return_value = None

        test_book_dao = BookDAO(driver=driver_mock)
        test_book_dao.driver.get = get_mock

        test_result = await test_book_dao.get_book_by_title(
            title='invalid_title',
        )

        assert test_result is None

    @pytest.mark.asyncio
    async def test_get_all_books__return_generator(self):
        driver_mock = mock.MagicMock

        async def generator_mock():
            values = (
                {
                    '_id': 0,
                    'author': 'test_author',
                    'title': 'test_title',
                },
                {
                    '_id': 1,
                    'author': 'test_author',
                },
            )
            for i in values:
                yield i

        get_all_mock = mock.AsyncMock(name='get_all_mock')
        get_all_mock.return_value = generator_mock()

        test_book_dao = BookDAO(driver=driver_mock)
        test_book_dao.driver.get_all = get_all_mock

        test_results = test_book_dao.get_all_books()

        assert [book async for book in test_results if book is not None]
