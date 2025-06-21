import pandas as pd
import logging
import time
from typing import Tuple

# ==========================================================
# Configure Logging
# ==========================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ==========================================================
# Main Transformation Function
# ==========================================================
def transform_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Cleans and normalizes the sales data.

    Args:
        df (pd.DataFrame): Raw sales data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            customers, stores, products, sales
    """
    logger.info("Starting data transformation...")

    # --- Drop duplicate and critical null transaction_ids ---
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["transaction_id"], inplace=True)

    # --- Handle missing 'day_of_week' ---
    if "day_of_week" in df.columns:
        modes = df["day_of_week"].mode()
        if not modes.empty:
            df["day_of_week"] = df["day_of_week"].fillna(modes[0])
        else:
            df.dropna(subset=["day_of_week"], inplace=True)

    # --- Drop rows missing critical categorical columns ---
    critical_cols = ["product_name", "product_category", "store_location", "customer_name"]
    df.dropna(subset=critical_cols, inplace=True)

    # --- Standardize text columns ---
    text_cols = ["product_name", "product_category", "store_location", "customer_name", "day_of_week"]
    title_case_columns = ["customer_name", "store_location", "day_of_week"]

    for col in text_cols:
        if col in df.columns and df[col].dtype == "object":
            df[col] = df[col].str.strip()
    for col in title_case_columns:
        if col in df.columns and df[col].dtype == "object":
            df[col] = df[col].str.title()

    # --- Validate duplicate transaction ids after cleaning ---
    dupes = df[df.duplicated(subset=["transaction_id"], keep=False)]
    if not dupes.empty:
        logger.warning(f"Found {len(dupes)} duplicate transaction_id rows. Dropping duplicates.")
        df.drop_duplicates(subset=["transaction_id"], inplace=True)

    # --- Fill missing price with mean price per product_name ---
    if "price" in df.columns:
        df["price"] = df.groupby("product_name")["price"].transform(lambda x: x.fillna(x.mean()))

    # --- Fill missing quantity_sold with average quantity, rounded to integer ---
    if "quantity_sold" in df.columns:
        df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce").fillna(df["quantity_sold"].mean())
        df["quantity_sold"] = df["quantity_sold"].round().astype(int)

    # --- Fill missing total_sale as price * quantity_sold ---
    if all(col in df.columns for col in ["total_sale", "price", "quantity_sold"]):
        df["total_sale"] = pd.to_numeric(df["total_sale"], errors="coerce")
        missing_total_sale = df["total_sale"].isnull()
        df.loc[missing_total_sale, "total_sale"] = (
            df.loc[missing_total_sale, "price"] * df.loc[missing_total_sale, "quantity_sold"]
        ).round(2)

    # --- Check for and nullify negative values in numeric columns ---
    for col in ["price", "quantity_sold", "total_sale"]:
        if col in df.columns:
            neg_values = df[df[col] < 0]
            if not neg_values.empty:
                logger.warning(f"Found {len(neg_values)} rows with negative {col}. Setting those to NaN.")
                df.loc[df[col] < 0, col] = pd.NA

    # --- Sanity check total_sale consistency ---
    if all(col in df.columns for col in ["price", "quantity_sold", "total_sale"]):
        inconsistent = df[abs(df["total_sale"] - df["price"] * df["quantity_sold"]) > 0.01]
        if not inconsistent.empty:
            logger.warning(f"{len(inconsistent)} rows with inconsistent total_sale values detected.")

    # Reset index after cleaning
    df.reset_index(drop=True, inplace=True)

    # ==========================================================
    # Creating Normalized Tables
    # ==========================================================
    logger.info("Creating normalized tables for customers, stores, products, and sales...")

    customers = df[["customer_name"]].drop_duplicates().reset_index(drop=True)
    customers["customer_id"] = customers.index + 1

    stores = df[["store_location"]].drop_duplicates().reset_index(drop=True)
    stores["store_id"] = stores.index + 1

    products = df[["product_name", "product_category"]].drop_duplicates().reset_index(drop=True)
    products["product_id"] = products.index + 1

    sales = (
        df.merge(customers, on="customer_name")
        .merge(stores, on="store_location")
        .merge(products, on=["product_name", "product_category"])
    )

    sales = sales[
        [
            "transaction_id",
            "day_of_week",
            "product_id",
            "customer_id",
            "store_id",
            "price",
            "quantity_sold",
            "total_sale",
        ]
    ]

    logger.info("Data transformation complete.")
    return customers, stores, products, sales


