import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.crypto.entity.config_entity import DataIngestionConfig
from src.crypto.entity.artifact_entity import DataIngestionArtifact
from src.crypto.exception import cryptoException
from src.crypto.logger import logging


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):

        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise cryptoException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Entered initiate_data_ingestion method")

        try:

            feature_store_path = (
                self.data_ingestion_config.feature_store_file_path
            )

            # create directory
            os.makedirs(
                os.path.dirname(feature_store_path),
                exist_ok=True
            )

            # create csv if missing
            if not os.path.exists(feature_store_path):

                dummy_df = pd.DataFrame({

    "open": list(range(100, 200)),

    "high": list(range(105, 205)),

    "low": list(range(95, 195)),

    "volume": list(range(1000, 1100)),

    "marketCap": list(range(50000, 50100)),

    "close": list(range(102, 202))
})

                dummy_df.to_csv(
                    feature_store_path,
                    index=False
                )

            # read dataset
            df = pd.read_csv(feature_store_path)

            logging.info(
                f"Dataset loaded successfully: {df.shape}"
            )

            # split dataset
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            # create output directories
            os.makedirs(
                os.path.dirname(
                    self.data_ingestion_config.training_file_path
                ),
                exist_ok=True
            )

            os.makedirs(
                os.path.dirname(
                    self.data_ingestion_config.testing_file_path
                ),
                exist_ok=True
            )

            # save train file
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False
            )

            # save test file
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False
            )

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=(
                    self.data_ingestion_config.training_file_path
                ),
                test_file_path=(
                    self.data_ingestion_config.testing_file_path
                )
            )

            logging.info(
                "Data ingestion completed successfully"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise cryptoException(e, sys)