import pandas as pd


class SensorModel:

    def __init__(self, preprocessing_object, trained_model_object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        try:
            # keep DataFrame structure
            if not isinstance(X, pd.DataFrame):
                X = pd.DataFrame(X)

            return self.trained_model_object.predict(X)

        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")