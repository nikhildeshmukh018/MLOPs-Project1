import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME  # We no longer need MONGODB_URL_KEY

# Load certificate authority file
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient handles MongoDB connections with a hardcoded connection string.

    Attributes:
    ----------
    client : MongoClient
        Shared MongoDB client instance.
    database : Database
        Selected database instance.
    """

    client = None  # Shared across all instances

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                # 🔒 Hardcoded MongoDB URL (for testing/dev only)
                mongo_db_url = "mongodb+srv://deshmukhnikhil018:7oyuo8YuQ3keAJdr@cluster0.onfz8rw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                
                # Validate URL
                if "<username>" in mongo_db_url or "<password>" in mongo_db_url:
                    raise Exception("MongoDB URL contains placeholders. Please replace with actual credentials.")
                
                # Establish connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("✅ MongoDB connection successful.")

        except Exception as e:
            raise MyException(e, sys)
