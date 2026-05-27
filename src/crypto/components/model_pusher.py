import sys
from src.crypto.cloud_storage.aws_storage import SimpleStorageService
from src.crypto.entity.config_entity import ModelPusherConfig
from src.crypto.entity.artifact_entity import ModelTrainerArtifact
from src.crypto.exception import cryptoException
from src.crypto.logger import logging


class ModelPusher:
    def __init__(self,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig = ModelPusherConfig(
                     bucket_name="your-s3-bucket-name",
                     s3_model_key_path="model/model.pkl",
                 )):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.model_pusher_config = model_pusher_config
            self.s3 = SimpleStorageService()

        except Exception as e:
            raise cryptoException(e, sys)

    def initiate_model_pusher(self):
        try:
            logging.info("Uploading model to AWS S3...")

            self.s3.upload_file(
                from_filename=self.model_trainer_artifact.trained_model_file_path,
                to_filename=self.model_pusher_config.s3_model_key_path,
                bucket_name=self.model_pusher_config.bucket_name,
            )

            logging.info("✅ Model uploaded successfully")

            return self.model_trainer_artifact

        except Exception as e:
            raise cryptoException(e, sys)
        