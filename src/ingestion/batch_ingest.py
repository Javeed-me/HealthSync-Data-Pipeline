"""
Batch ingestion module for healthcare data.
Reads healthcare dataset from CSV and stores raw data in Bronze layer.
"""

import pandas as pd
from src.utils.config import SAMPLE_CSV, BRONZE_DIR, LARGE_CSV
from src.utils.logging import get_logger

logger = get_logger(__name__)

def ingest_batch_data(use_large: bool = False):
    """
    Ingest batch healthcare data from CSV to Bronze layer.
    
    Args:
        use_large: If True, use the large generated dataset (healthcare_large.csv)
                   If False, use the sample dataset (sample_healthcare.csv)
    """
    try:
        logger.info("Starting batch ingestion for healthcare data")

        # Select input file
        input_csv = LARGE_CSV if use_large else SAMPLE_CSV
        
        # Read CSV using pandas
        df = pd.read_csv(input_csv)
        logger.info(f"Read {len(df)} rows from {input_csv}")

        # Save to Bronze layer as CSV
        output_path = f"{BRONZE_DIR}/batch_healthcare_data.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Data written to Bronze layer at {output_path}")

    except Exception as e:
        logger.error(f"Error in batch ingestion: {str(e)}")
        raise

if __name__ == "__main__":
    ingest_batch_data()