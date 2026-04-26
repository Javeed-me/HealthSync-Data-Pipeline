"""
Batch ingestion module.
Reads data from CSV file and stores raw data in Bronze layer as Parquet.
"""

import pandas as pd
from pyspark.sql import SparkSession
from src.utils.config import SAMPLE_CSV, BRONZE_DIR, SPARK_APP_NAME
from src.utils.logging import get_logger

logger = get_logger(__name__)

def ingest_batch_data():
    """Ingest batch data from CSV to Bronze layer."""
    try:
        logger.info("Starting batch ingestion")

        # Initialize Spark session
        spark = SparkSession.builder.appName(SPARK_APP_NAME).getOrCreate()

        # Read CSV using pandas
        df_pd = pd.read_csv(SAMPLE_CSV)
        logger.info(f"Read {len(df_pd)} rows from CSV")

        # Convert to Spark DataFrame
        df_spark = spark.createDataFrame(df_pd)

        # Write to Bronze layer as Parquet
        output_path = f"{BRONZE_DIR}/batch_data"
        df_spark.write.mode("overwrite").parquet(output_path)
        logger.info(f"Data written to Bronze layer at {output_path}")

        spark.stop()
        logger.info("Batch ingestion completed successfully")

    except Exception as e:
        logger.error(f"Error in batch ingestion: {str(e)}")
        raise

if __name__ == "__main__":
    ingest_batch_data()