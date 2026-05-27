import sys
import numpy as np

from sklearn.metrics import r2_score

from src.crypto.exception import cryptoException
from src.crypto.logger import logging
from src.crypto.utils.main_utils import load_numpy_array_data, load_object

from src.crypto.entity.artifact_entity import ModelEvaluationArtifact


class ModelEvaluation:

    def __init__(self, model_eval_config, data_transformation_artifact, model_trainer_artifact):
        self.model_eval_config = model_eval_config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_evaluation(self):

        try:
            logging.info("Loading test data")

            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            logging.info("Loading trained model")

            model_wrapper = load_object(
                self.model_trainer_artifact.trained_model_file_path
            )

            y_pred = model_wrapper.trained_model_object.predict(X_test)

            r2 = r2_score(y_test, y_pred)

            logging.info(f"R2 Score: {r2}")

            expected_score = self.model_eval_config.expected_score

            is_model_accepted = r2 >= expected_score

            return ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                changed_accuracy=r2,
                best_model_path=self.model_trainer_artifact.trained_model_file_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path
            )

        except Exception as e:
            raise cryptoException(e, sys) from e