import pandas as pd
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

  # ==========================================================
# Extracting the data
# ==========================================================
def extract_data() -> pd.DataFrame:
    """Extracts data from Mockaroo API and returns a DataFrame."""
    logger.info("Starting data extraction from Mockaroo API...")
    api = "https://api.mockaroo.com/api/0935e020?count=200&key=d34db810"
    start_time = time.perf_counter()
    try:
        df = pd.read_csv(api)
        elapsed = time.perf_counter() - start_time
        logger.info(f"Extracted {len(df)} records in {elapsed:.2f} seconds")
        return df
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise

