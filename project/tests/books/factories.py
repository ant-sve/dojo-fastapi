import factory

from books.schemas import DBBookSchema


class DBBookFactory(factory.Factory):

    class Meta:
        model = DBBookSchema

    _id = factory.Sequence(lambda n: n)
    author = factory.Faker('name')
    title = factory.Faker('catch_phrase')
