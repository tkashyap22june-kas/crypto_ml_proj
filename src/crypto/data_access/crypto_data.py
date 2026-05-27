import pandas as pd
from src.crypto.configuration.Mongo_db_connection import MongoDBClient


class cryptoData:

    def __init__(self):

        self.mongo_client = MongoDBClient().database

    def export_collection_as_dataframe(self, collection_name):

        try:

            collection = self.mongo_client[collection_name]

            df = pd.DataFrame(list(collection.find()))

            print("\n========== DEBUG ==========")
            print("Collection Name:", collection_name)
            print("Dataframe Shape:", df.shape)
            print(df.head())
            print("===========================\n")

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            return df

        except Exception as e:
            raise e