import os

from dotenv import load_dotenv

load_dotenv()

DATABASE: str = os.getenv('DATABASE_NAME')
MONGO_HOST: str = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT: str = os.getenv('MONGO_PORT', 27017)
COLLECTION: str = os.getenv('COLLECTION_NAME')
TELEGRAM_BOT_TOKEN: str = os.getenv('BOT_TOKEN')
