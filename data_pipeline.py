import logging
from extract import extract_data
from transform import transform_data
from load import upload_df_to_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 1. Extract
    df_raw = extract_data()

    # 2. Transformc
    customers, stores, products, sales = transform_data(df_raw)

    # 3. Load (upload to S3)
    bucket_name = "databucket-v1"
    upload_df_to_s3(customers, bucket_name, "transformed_data/customers.csv")
    upload_df_to_s3(stores, bucket_name, "transformed_data/stores.csv")
    upload_df_to_s3(products, bucket_name, "transformed_data/products.csv")
    upload_df_to_s3(sales, bucket_name, "transformed_data/sales.csv")

if __name__ == "__main__":
    main()
