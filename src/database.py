import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_config = Database()

async def connect_db():
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise Exception("MONGODB_URI not found in environment variables")
    
    db_config.client = AsyncIOMotorClient(mongodb_uri)
    # Extract DB name from URI or use default
    db_name = mongodb_uri.split("/")[-1].split("?")[0] or "rag_app"
    db_config.db = db_config.client[db_name]

def get_db():
    return db_config.db
