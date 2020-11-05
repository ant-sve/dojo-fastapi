import pytest


@pytest.fixture
def test_app():
    from app import app

    return app
