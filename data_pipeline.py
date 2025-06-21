import logging
import os
from extract import extract_data
from transform import transform_data
from load import upload_df_to_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def main():
    try:
        # 1. Extract
        df_raw = extract_data()

        # 2. Transform
        customers, stores, products, sales = transform_data(df_raw)

        # 3. Load (upload to S3)
        bucket_name = os.getenv("S3_BUCKET_NAME")  # No hardcoded fallback
        if not bucket_name:
            raise ValueError("Missing S3_BUCKET_NAME environment variable.")

        upload_df_to_s3(df_raw, bucket_name, "raw_data/raw_sales.csv")
        upload_df_to_s3(customers, bucket_name, "transformed_data/customers.csv")
        upload_df_to_s3(stores, bucket_name, "transformed_data/stores.csv")
        upload_df_to_s3(products, bucket_name, "transformed_data/products.csv")
        upload_df_to_s3(sales, bucket_name, "transformed_data/sales.csv")

        logger.info("✅ Pipeline completed successfully!")
    except Exception as e:
        logger.error(f"❌ pipeline failed: {e}")
        raise  # Re-raise if you want the error to propagate

if __name__ == "__main__":
    main()
