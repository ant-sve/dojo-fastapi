from typing import AsyncGenerator, Optional

from pydantic import ValidationError

from .schemas import DBBookSchema, BaseBookSchema


class BookDAO:

    def __init__(self, driver, collection_name: str = 'books'):
        self.collection_name = collection_name
        self.driver = driver(collection_name)

    async def get_book_by_title(self, title: str) -> DBBookSchema:
        document = await self.driver.get(title=title)

        if document is not None:
            entity = DBBookSchema(**document)
        else:
            entity = None

        return entity

    async def get_all_books(
            self,
            ) -> AsyncGenerator[Optional[DBBookSchema], None]:
        documents = await self.driver.get_all()

        async for document in documents:

            try:
                entity = DBBookSchema(**document)
            except ValidationError as e:
                entity = None

                # TODO: logging

            yield entity

    async def insert_one_book(self, new_book: BaseBookSchema) -> bool:
        result = await self.driver.insert_one(new_book.dict())

        return True if result.acknowledged else False

    async def replace_one_book_by_title(
            self,
            title: str,
            new_book: BaseBookSchema,
            ) -> int:
        result = await self.driver.replace_one(
            data=new_book.dict(),
            title=title,
        )

        return result.modified_count

    async def remove_one_book_by_title(self, title: str) -> int:
        result = await self.driver.delete_one(title=title)

        return result.deleted_count
