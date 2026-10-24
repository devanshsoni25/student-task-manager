import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from .env file")

mongodb_client = AsyncMongoClient(MONGODB_URI)

db = mongodb_client["student-data"]

CollectionUser = db["users"]
CollectionTask = db["tasks"]