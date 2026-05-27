from io import StringIO
from pandas import DataFrame, read_csv
import os
import sys
import pickle
import shutil

from src.crypto.exception import cryptoException


class SimpleStorageService:

    def __init__(self):
        pass

    def get_bucket(self, bucket_name: str):
        return None

    def s3_key_path_available(
        self,
        bucket_name: str,
        s3_key: str
    ) -> bool:
        return os.path.exists(s3_key)

    @staticmethod
    def read_object(
        object_name,
        decode: bool = True,
        make_readable: bool = False
    ):
        try:
            mode = "rb" if not decode else "r"

            with open(object_name, mode) as f:
                body = f.read()

            if decode and make_readable:
                body = StringIO(body)

            return body

        except Exception as e:
            raise cryptoException(e, sys)

    def get_file_object(
        self,
        filename: str,
        bucket_name: str
    ):
        try:
            if not os.path.exists(filename):
                raise cryptoException(
                    f"{filename} not found locally",
                    sys
                )

            return filename

        except Exception as e:
            raise cryptoException(e, sys)

    def load_model(
        self,
        model_name: str,
        bucket_name: str,
        model_dir: str = None
    ):
        try:
            model_file = (
                model_name
                if model_dir is None
                else f"{model_dir}/{model_name}"
            )

            with open(model_file, "rb") as f:
                return pickle.load(f)

        except Exception as e:
            raise cryptoException(e, sys)

    def get_df_from_object(
        self,
        object_
    ) -> DataFrame:
        try:
            content = self.read_object(
                object_,
                make_readable=True
            )

            return read_csv(content)

        except Exception as e:
            raise cryptoException(e, sys)

    def read_csv(
        self,
        filename: str,
        bucket_name: str
    ) -> DataFrame:
        try:
            return read_csv(filename)

        except Exception as e:
            raise cryptoException(e, sys)

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = False
    ):
        try:
            folder = os.path.dirname(to_filename)

            if folder:
                os.makedirs(folder, exist_ok=True)

            shutil.copy(from_filename, to_filename)

            if remove:
                os.remove(from_filename)

        except Exception as e:
            raise cryptoException(e, sys)

    def download_file(
        self,
        bucket_name: str,
        s3_key: str,
        local_path: str
    ):
        try:
            folder = os.path.dirname(local_path)

            if folder:
                os.makedirs(folder, exist_ok=True)

            shutil.copy(s3_key, local_path)

        except Exception as e:
            raise cryptoException(e, sys)