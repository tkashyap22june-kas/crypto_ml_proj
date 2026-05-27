import sys
import pandas as pd
from pandas import DataFrame

from src.crypto.exception import cryptoException
from src.crypto.logger import logging
from src.crypto.utils.main_utils import read_yaml_file
from src.crypto.constant.training_pipeline import SCHEMA_FILE_PATH

from src.crypto.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)

from src.crypto.entity.config_entity import DataValidationConfig


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):

        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config

        self._schema_config = read_yaml_file(
            file_path=SCHEMA_FILE_PATH
        )

    def validate_number_of_columns(
        self,
        dataframe: DataFrame
    ) -> bool:

        try:

            status = len(dataframe.columns) == len(
                self._schema_config["columns"]
            )

            logging.info(
                f"Required columns present status: {status}"
            )

            return status

        except Exception as e:
            raise cryptoException(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:

        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise cryptoException(e, sys)

    def is_numerical_column_exist(
        self,
        df: DataFrame
    ) -> bool:

        try:

            dataframe_columns = df.columns

            status = True

            missing_numerical_columns = []

            for column in self._schema_config["numerical_columns"]:

                if column not in dataframe_columns:

                    status = False

                    missing_numerical_columns.append(column)

            logging.info(
                f"Missing numerical columns: {missing_numerical_columns}"
            )

            return status

        except Exception as e:
            raise cryptoException(e, sys)

    def initiate_data_validation(
        self
    ) -> DataValidationArtifact:

        logging.info(
            "Entered initiate_data_validation method"
        )

        try:

            validation_error_msg = ""

            train_df = DataValidation.read_data(
                file_path=self.data_ingestion_artifact.trained_file_path
            )

            test_df = DataValidation.read_data(
                file_path=self.data_ingestion_artifact.test_file_path
            )

            # validate column count
            status = self.validate_number_of_columns(
                dataframe=train_df
            )

            if not status:
                validation_error_msg += (
                    "Columns missing in training dataframe. "
                )

            status = self.validate_number_of_columns(
                dataframe=test_df
            )

            if not status:
                validation_error_msg += (
                    "Columns missing in testing dataframe. "
                )

            # validate numerical columns
            status = self.is_numerical_column_exist(
                df=train_df
            )

            if not status:
                validation_error_msg += (
                    "Numerical columns missing in training dataframe. "
                )

            status = self.is_numerical_column_exist(
                df=test_df
            )

            if not status:
                validation_error_msg += (
                    "Numerical columns missing in testing dataframe. "
                )

            validation_status = (
                len(validation_error_msg) == 0
            )

            data_validation_artifact = DataValidationArtifact(

                validation_status=validation_status,

                valid_train_file_path=(
                    self.data_ingestion_artifact.trained_file_path
                ),

                valid_test_file_path=(
                    self.data_ingestion_artifact.test_file_path
                ),

                invalid_train_file_path=(
                    self.data_validation_config.invalid_train_file_path
                ),

                invalid_test_file_path=(
                    self.data_validation_config.invalid_test_file_path
                ),

                drift_report_file_path=(
                    self.data_validation_config.drift_report_file_path
                )
            )

            logging.info(
                f"Data validation artifact: {data_validation_artifact}"
            )

            return data_validation_artifact

        except Exception as e:
            raise cryptoException(e, sys)
