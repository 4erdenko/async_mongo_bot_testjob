import motor.motor_asyncio

from config import COLLECTION, DATABASE, MONGO_HOST, MONGO_PORT


class MongoBase:
    def __init__(self):
        connection_string = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATABASE}'
        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self.db = self.client[DATABASE]
        self.collection = self.db[COLLECTION]

    async def aggregate(self, pipeline: list):
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=None)
