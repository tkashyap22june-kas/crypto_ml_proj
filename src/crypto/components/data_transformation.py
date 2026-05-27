import sys
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

from src.crypto.constant.training_pipeline import TARGET_COLUMN, SCHEMA_FILE_PATH
from src.crypto.entity.config_entity import DataTransformationConfig
from src.crypto.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact
)

from src.crypto.exception import cryptoException
from src.crypto.logger import logging
from src.crypto.utils.main_utils import (
    save_object,
    save_numpy_array_data,
    read_yaml_file
)


class DataTransformation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_config: DataTransformationConfig
    ):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise cryptoException(e, sys)

    # =========================
    # FEATURE CLEANING (IMPORTANT)
    # =========================
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Cleaning dataframe (dropping unwanted columns)")

            drop_cols = ["Unnamed: 0", "date", "timestamp", "crypto_name"]

            df = df.drop(columns=drop_cols, errors="ignore")

            return df

        except Exception as e:
            raise cryptoException(e, sys)

    # =========================
    # PREPROCESSOR
    # =========================
    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            logging.info("Loading schema file")
            schema = read_yaml_file(SCHEMA_FILE_PATH)

            num_features = schema["numerical_columns"]
            cat_features = schema.get("categorical_columns", [])

            logging.info(f"Numerical features: {num_features}")
            logging.info(f"Categorical features: {cat_features}")

            numeric_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent"))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_pipeline, num_features),
                    ("cat", categorical_pipeline, cat_features)
                ],
                remainder="drop"
            )

            return preprocessor

        except Exception as e:
            raise cryptoException(e, sys)

    # =========================
    # MAIN TRANSFORMATION
    # =========================
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            # CLEAN DATA FIRST
            train_df = self._clean_dataframe(train_df)
            test_df = self._clean_dataframe(test_df)

            schema = read_yaml_file(SCHEMA_FILE_PATH)

            feature_cols = schema["numerical_columns"] + schema.get("categorical_columns", [])

            # SAFETY CHECK (VERY IMPORTANT)
            missing_cols = set(feature_cols) - set(train_df.columns)
            if missing_cols:
                raise Exception(f"Missing columns in dataset: {missing_cols}")

            # SPLIT FEATURES/TARGET
            input_train = train_df[feature_cols]
            input_test = test_df[feature_cols]

            target_train = train_df[TARGET_COLUMN]
            target_test = test_df[TARGET_COLUMN]

            # PREPROCESSOR
            preprocessor = self.get_data_transformer_object()

            input_train_arr = preprocessor.fit_transform(input_train)
            input_test_arr = preprocessor.transform(input_test)

            # COMBINE FEATURES + TARGET
            train_arr = np.c_[input_train_arr, target_train.to_numpy()]
            test_arr = np.c_[input_test_arr, target_test.to_numpy()]

            # SAVE ARTIFACTS
            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor
            )

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            logging.info("Data transformation completed successfully")

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise cryptoException(e, sys) from e