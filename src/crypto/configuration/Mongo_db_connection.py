import sys
from src.crypto.exception import cryptoException


import os
from src.crypto.constant.database import DATABASE_NAME
import pymongo
import certifi
from dotenv import load_dotenv

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL")
                if mongo_db_url is None:
                    raise Exception(f"Environment key is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise cryptoException(e,sys)