import sys
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.crypto.exception import cryptoException
from src.crypto.logger import logging
from src.crypto.utils.main_utils import (
    load_numpy_array_data,
    load_object,
    save_object
)

from src.crypto.entity.config_entity import ModelTrainerConfig
from src.crypto.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    RegressionMetricArtifact
)

from src.crypto.entity.estimator import SensorModel


class ModelTrainer:

    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:
            logging.info("Loading training and testing data")

            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model = LinearRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))

            preprocessing_obj = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )

            sensor_model = SensorModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=model
            )

            save_object(self.model_trainer_config.trained_model_file_path, sensor_model)

            metric_artifact = RegressionMetricArtifact(
                r2_score=r2,
                mae=mae,
                rmse=rmse
            )

            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )

        except Exception as e:
            raise cryptoException(e, sys) from e
