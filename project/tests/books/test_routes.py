import unittest.mock as mock


class TestBooksRoutes:

    def test_get_all_books__no_input__return_list(
            self,
            books_test_client,
            books_dao_mock,
            ):

        async def get_books():
            yield None

        books_dao_mock.get_all_books.return_value = get_books()

        test_response = books_test_client.get('/api/books/all')

        assert test_response.status_code == 200
        assert isinstance(test_response.json(), list)

    def test_get_book__valid_title__return_json(
            self,
            books_test_client,
            books_dao_mock,
            db_book_and_external_json,
            ):
        db_book, exteranl_json = db_book_and_external_json

        books_dao_mock.get_book_by_title = mock.AsyncMock(
            return_value=db_book,
        )

        test_response = books_test_client.get('/api/books/?title=test')

        assert test_response.status_code == 200
        assert test_response.json() == exteranl_json

    def test_create_one__valid_json__return_json(
            self,
            books_test_client,
            books_dao_mock,
            db_book_and_external_json,
            ):
        test_value = True
        _, exteranl_json = db_book_and_external_json

        books_dao_mock.insert_one_book = mock.AsyncMock(
            return_value=test_value,
        )

        test_response = books_test_client.post(
            '/api/books/',
            json=exteranl_json,
        )

        assert test_response.status_code == 200
        assert test_response.json() == {'inserted': test_value}

    def test_update_one__valid_title_and_json__return_json(
            self,
            books_test_client,
            books_dao_mock,
            db_book_and_external_json,
            ):
        test_modified_counter = 1
        _, exteranl_json = db_book_and_external_json

        books_dao_mock.replace_one_book_by_title = mock.AsyncMock(
            return_value=test_modified_counter,
        )

        test_response = books_test_client.put(
            '/api/books/?title=test',
            json=exteranl_json,
        )

        assert test_response.status_code == 200
        assert test_response.json() == {'modified': test_modified_counter}

    def test_remove_one__valid_title__return_json(
            self,
            books_test_client,
            books_dao_mock,
            ):
        test_removed_counter = 1
        books_dao_mock.remove_one_book_by_title = mock.AsyncMock(
            return_value=test_removed_counter,
        )

        test_response = books_test_client.delete('/api/books/?title=test')

        assert test_response.status_code == 200
        assert test_response.json() == {'removed': test_removed_counter}
