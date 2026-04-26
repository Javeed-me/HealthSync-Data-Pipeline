"""
Data transformation module using Pandas.
Processes data from Bronze to Silver to Gold layers with healthcare validations.
"""

import pandas as pd
from src.processing.quality import validate_data_quality
from src.processing.healthcare_validations import flag_abnormal_vitals
from src.utils.config import BRONZE_DIR, SILVER_DIR, GOLD_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)

def bronze_to_silver(input_path: str) -> pd.DataFrame:
    """Transform raw Bronze data to cleaned Silver data."""
    logger.info(f"Reading Bronze data from {input_path}")
    df = pd.read_csv(input_path)

    # Validate quality
    if not validate_data_quality(df):
        raise ValueError("Data quality check failed for Bronze data")

    # Clean transformations: fill nulls with defaults
    df = df.fillna({
        'heart_rate': 70,  # Default normal
        'temperature': 37.0,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80
    })

    # Apply healthcare validations
    df = flag_abnormal_vitals(df)

    logger.info("Bronze to Silver transformation completed")
    return df

def silver_to_gold(df_silver: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Silver data to Gold layer: average vitals per patient."""
    # Ensure numeric columns are properly typed
    numeric_cols = ['heart_rate', 'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic']
    for col in numeric_cols:
        df_silver[col] = pd.to_numeric(df_silver[col], errors='coerce')

    df_gold = df_silver.groupby('patient_id').agg({
        'heart_rate': 'mean',
        'temperature': 'mean',
        'blood_pressure_systolic': 'mean',
        'blood_pressure_diastolic': 'mean',
        'any_abnormal': 'sum'  # Count of abnormal records per patient
    }).reset_index()

    # Rename columns
    df_gold.columns = ['patient_id', 'avg_heart_rate', 'avg_temperature', 'avg_bp_systolic', 'avg_bp_diastolic', 'abnormal_count']

    logger.info("Silver to Gold aggregation completed")
    return df_gold

def process_data(input_path: str, layer: str = "batch"):
    """Main processing function."""
    try:
        logger.info(f"Starting data processing for {layer}")

        # Bronze to Silver
        df_silver = bronze_to_silver(input_path)
        silver_path = f"{SILVER_DIR}/{layer}_healthcare_data.csv"
        df_silver.to_csv(silver_path, index=False)
        logger.info(f"Silver data written to {silver_path}")

        # Silver to Gold
        df_gold = silver_to_gold(df_silver)
        gold_path = f"{GOLD_DIR}/{layer}_healthcare_data.csv"
        df_gold.to_csv(gold_path, index=False)
        logger.info(f"Gold data written to {gold_path}")

        logger.info("Data processing completed")

    except Exception as e:
        logger.error(f"Error in data processing: {str(e)}")
        raise

if __name__ == "__main__":
    # Example: process batch data
    batch_input = f"{BRONZE_DIR}/batch_healthcare_data.csv"
    process_data(batch_input, "batch")