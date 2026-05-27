import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class S3Client:

    s3_client = None
    s3_resource = None

    def __init__(self, region_name=None):

        region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

        if S3Client.s3_resource is None or S3Client.s3_client is None:

            access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if not access_key_id:
                raise Exception("Environment variable AWS_ACCESS_KEY_ID is not set.")

            if not secret_access_key:
                raise Exception("Environment variable AWS_SECRET_ACCESS_KEY is not set.")

            S3Client.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name,
            )

            S3Client.s3_client = boto3.client(
                "s3",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name,
            )

        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client