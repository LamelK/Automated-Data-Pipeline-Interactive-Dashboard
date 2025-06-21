import boto3
import logging
import time
import io
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_df_to_s3(df: pd.DataFrame, bucket: str, key: str):
    """
    Uploads a pandas DataFrame as CSV directly to an S3 bucket.

    Args:
        df (pd.DataFrame): DataFrame to upload.
        bucket (str): S3 bucket name.
        key (str): S3 object key (including folders and filename, e.g. 'folder/file.csv').
    """
    start_time = time.perf_counter()
    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        elapsed = time.perf_counter() - start_time
        logger.info(f"Uploaded DataFrame to s3://{bucket}/{key} in {elapsed:.2f} seconds")
    except Exception as e:
        logger.error(f"Failed to upload DataFrame to S3: {e}")
        raise


