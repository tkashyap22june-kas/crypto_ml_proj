from src.crypto.cloud_storage.aws_storage import SimpleStorageService

BUCKET_NAME = "your-bucket-name"

s3 = SimpleStorageService()

print(
    s3.s3_key_path_available(
        BUCKET_NAME,
        "artifact/"
    )
)