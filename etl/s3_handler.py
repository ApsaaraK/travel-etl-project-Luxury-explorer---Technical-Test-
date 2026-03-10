import boto3
import os
from dotenv import load_dotenv
from etl.logger import get_logger

load_dotenv()
logger = get_logger("s3_handler")

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

def upload_to_s3(local_filepath, s3_key):
    bucket = os.getenv("AWS_BUCKET_NAME")
    s3 = get_s3_client()

    logger.info(f"Uploading {local_filepath} to s3://{bucket}/{s3_key}")
    s3.upload_file(local_filepath, bucket, s3_key)
    logger.info(f"Upload successful: s3://{bucket}/{s3_key}")