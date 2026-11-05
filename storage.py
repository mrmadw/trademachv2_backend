import os
import boto3
from botocore.config import Config

s3_client = boto3.client(
    "s3",
    endpoint_url=os.environ["GARAGE_ENDPOINT"],
    aws_access_key_id=os.environ["GARAGE_KEY_ID"],
    aws_secret_access_key=os.environ["GARAGE_SECRET_KEY"],
    region_name=os.getenv("GARAGE_REGION", "garage"),
    config=Config(
        signature_version="s3v4"
    )
)

BUCKET_NAME = os.environ["GARAGE_BUCKET"]


def generate_image_url(image_key):
    if not image_key:
        return None

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": image_key
        },
        ExpiresIn=3600
    )