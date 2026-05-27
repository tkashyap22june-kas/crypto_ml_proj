from crypto.configuration.Mongo_db_connection import *
from crypto.configuration.aws_connection import *


class DataIngestionConfig:

    def __init__(self):

        self.feature_store_file_path = (
            "artifact/feature_store/data.csv"
        )

        self.training_file_path = (
            "artifact/train.csv"
        )

        self.testing_file_path = (
            "artifact/test.csv"
        )

        self.train_test_split_ratio = 0.2

        self.collection_name = "crypto_data"


class DataValidationConfig:

    def __init__(self):

        self.invalid_train_file_path = (
            "artifact/data_validation/invalid_train.csv"
        )

        self.invalid_test_file_path = (
            "artifact/data_validation/invalid_test.csv"
        )

        self.valid_train_file_path = (
            "artifact/data_validation/valid_train.csv"
        )

        self.valid_test_file_path = (
            "artifact/data_validation/valid_test.csv"
        )

        self.drift_report_file_path = (
            "artifact/data_validation/drift_report.yaml"
        )


class DataTransformationConfig:

    def __init__(self):

        self.transformed_object_file_path = (
            "artifact/data_transformation/preprocessor.pkl"
        )

        self.transformed_train_file_path = (
            "artifact/data_transformation/train.npy"
        )

        self.transformed_test_file_path = (
            "artifact/data_transformation/test.npy"
        )


class ModelTrainerConfig:

    def __init__(self):

        self.trained_model_file_path = (
            "artifact/model_trainer/model.pkl"
        )

        self.expected_accuracy = 0.6

        self.overfitting_underfitting_threshold = 0.1


class ModelEvaluationConfig:

    def __init__(self):

        self.expected_score = 0.6

        self.overfitting_underfitting_threshold = 0.1


class ModelPusherConfig:

    def __init__(self):

        self.s3_model_key_path = (
            "model-registry/model.pkl"
        )

        self.bucket_name = (
            "crypto-ml-models"
        )


class TrainingPipelineConfig:

    def __init__(self):

        self.data_ingestion_config = (
            DataIngestionConfig()
        )

        self.data_validation_config = (
            DataValidationConfig()
        )

        self.data_transformation_config = (
            DataTransformationConfig()
        )

        self.model_trainer_config = (
            ModelTrainerConfig()
        )

        self.model_evaluation_config = (
            ModelEvaluationConfig()
        )

        self.model_pusher_config = (
            ModelPusherConfig()
        )


class ConfigurationManager:

    def __init__(self):

        print("ConfigurationManager Loaded")

    def get_training_pipeline_config(self):

        return TrainingPipelineConfig()