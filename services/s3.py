import os
import boto3
from botocore.config import Config


s3 = boto3.client(
    "s3",
    region_name=os.environ["AWS_REGION"],
    endpoint_url=f"https://s3.{os.environ['AWS_REGION']}.amazonaws.com",
    config=Config(signature_version="s3v4", s3={"addressing_style": "virtual"}),
)

BUCKET = os.environ["S3_BUCKET"]

def image_url(key, expires=3600):
    if not key:
        return None
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )