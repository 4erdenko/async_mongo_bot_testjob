from typing import List

from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

from config import COLLECTION, DATABASE, MONGO_HOST, MONGO_PORT


class MongoBase:
    def __init__(self) -> None:
        connection_string: str = (
            f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATABASE}'
        )
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(connection_string)
        self.db: AsyncIOMotorDatabase = self.client[DATABASE]
        self.collection: AsyncIOMotorCollection = self.db[COLLECTION]

    async def aggregate(self, pipeline: List[dict]) -> List[dict]:
        return await self.collection.aggregate(pipeline).to_list(length=None)
