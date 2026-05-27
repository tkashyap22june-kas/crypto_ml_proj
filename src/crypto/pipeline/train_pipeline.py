import sys
from crypto.components.data_ingestion import DataIngestion
from crypto.components.data_validation import DataValidation
from crypto.components.data_transformation import DataTransformation
from crypto.components.model_trainer import ModelTrainer
from crypto.components.model_evaluation import ModelEvaluation
from crypto.components.model_pusher import ModelPusher
from crypto.configuration.configuration import ConfigurationManager
from crypto.exception import cryptoException
from crypto.logger import logging

from crypto.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)

from crypto.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact
)


class TrainPipeline:

    def __init__(self):
        self.config = ConfigurationManager().get_training_pipeline_config()
        self.data_ingestion_config = self.config.data_ingestion_config
        self.data_validation_config = self.config.data_validation_config
        self.data_transformation_config = self.config.data_transformation_config
        self.model_trainer_config = self.config.model_trainer_config
        self.model_evaluation_config = self.config.model_evaluation_config
        self.model_pusher_config = self.config.model_pusher_config

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")

            data_ingestion = DataIngestion(self.data_ingestion_config)
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            return data_validation.initiate_data_validation()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def start_data_transformation(self, data_ingestion_artifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config
            )
            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def start_model_trainer(self, data_transformation_artifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            return model_trainer.initiate_model_trainer()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def start_model_evaluation(self, data_transformation_artifact, model_trainer_artifact) -> ModelEvaluationArtifact:
        try:
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            return model_evaluation.initiate_model_evaluation()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def start_model_pusher(self, model_trainer_artifact):
        try:
            model_pusher = ModelPusher(
                model_trainer_artifact=model_trainer_artifact,
                model_pusher_config=self.model_pusher_config
            )
            return model_pusher.initiate_model_pusher()

        except Exception as e:
            raise cryptoException(e, sys) from e

    def run_pipeline(self):
        try:
            logging.info("Pipeline started")

            ingestion = self.start_data_ingestion()
            validation = self.start_data_validation(ingestion)
            transformation = self.start_data_transformation(ingestion)

            trainer = self.start_model_trainer(transformation)

            evaluation = self.start_model_evaluation(
                transformation,
                trainer
            )

            if not evaluation.is_model_accepted:
                logging.info("Model rejected")
                return

            self.start_model_pusher(trainer)

            logging.info("Pipeline completed successfully")

        except Exception as e:
            raise cryptoException(e, sys) from e


if __name__ == "__main__":
    obj = TrainPipeline()
    obj.run_pipeline()



