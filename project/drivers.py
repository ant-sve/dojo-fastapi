import motor.motor_asyncio
import settings

from typing import Dict, Any

from motor.motor_asyncio import AsyncIOMotorCursor
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class MongoDriver:

    connection_args = {
        'compressors': 'zlib',
        'zlibCompressionLevel': 7,
    }

    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI,
        **connection_args,
    )
    db = client.get_database(settings.MONGO_DB)

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection = self.db.get_collection(self.collection_name)

    async def get(self, **query) -> Dict[str, Any]:
        document = await self.collection.find_one(query)

        return document

    async def get_all(self) -> AsyncIOMotorCursor:
        documents = self.collection.find()

        return documents

    async def insert_one(self, data: Dict[str, Any]) -> InsertOneResult:
        result = await self.collection.insert_one(data)

        return result

    async def replace_one(self, data: Dict[str, Any], **query) -> UpdateResult:
        result = await self.collection.replace_one(
            filter=query,
            replacement=data,
        )

        return result

    async def delete_one(self, **query) -> DeleteResult:
        result = await self.collection.delete_one(filter=query)

        return result
