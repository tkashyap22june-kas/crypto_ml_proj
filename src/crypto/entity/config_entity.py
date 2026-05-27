from dataclasses import dataclass


# =========================
# Data Ingestion
# =========================
@dataclass
class DataIngestionConfig:
    collection_name: str
    database_name: str
    data_ingestion_dir: str
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str
    train_test_split_ratio: float


# =========================
# Data Validation
# =========================
@dataclass
class DataValidationConfig:
    data_validation_dir: str
    valid_train_file_path: str
    valid_test_file_path: str

    invalid_train_file_path: str
    invalid_test_file_path: str

    drift_report_file_path: str


# =========================
# Data Transformation
# =========================
@dataclass
class DataTransformationConfig:
    data_transformation_dir: str
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str


# =========================
# Model Trainer
# =========================
@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str
    trained_model_file_path: str
    expected_accuracy: float
    overfitting_underfitting_threshold: float


# =========================
# Model Evaluation
# =========================
@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float
    bucket_name: str
    s3_model_key_path: str


# =========================
# Model Pusher
# =========================
@dataclass
class ModelPusherConfig:
    bucket_name: str
    s3_model_key_path: str