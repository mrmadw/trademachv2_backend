import os
import boto3
from botocore.config import Config

_cfg = Config(
    signature_version="s3v4",
    s3={"addressing_style": "path"},
)


def _make_client(endpoint):
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ["GARAGE_KEY_ID"],
        aws_secret_access_key=os.environ["GARAGE_SECRET_KEY"],
        region_name=os.getenv("GARAGE_REGION", "garage"),
        config=_cfg,
    )


# Server-side operations (upload, delete, head) over the Docker network
s3_client = _make_client(os.environ["GARAGE_ENDPOINT"])

# Used only to sign URLs that browsers will open
s3_public_client = _make_client(
    os.getenv("GARAGE_PUBLIC_ENDPOINT") or os.environ["GARAGE_ENDPOINT"]
)

BUCKET_NAME = os.environ["GARAGE_BUCKET"]


def generate_image_url(image_key):
    if not image_key:
        return None

    return s3_public_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": image_key},
        ExpiresIn=3600,
    )