"""
Streaming simulation module for healthcare data.
Simulates real-time patient vitals using Python generator and appends to Bronze layer.
"""

import pandas as pd
import random
import time
from datetime import datetime, timedelta
from src.utils.config import BRONZE_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)

def generate_vital_data(patient_id: int, base_timestamp: datetime):
    """Generate a single vital data record."""
    # Random vitals, sometimes abnormal
    heart_rate = random.randint(30, 200)  # Some abnormal
    temperature = round(random.uniform(34.0, 43.0), 1)  # Some abnormal
    systolic = random.randint(90, 160)
    diastolic = random.randint(60, 100)

    timestamp = base_timestamp + timedelta(seconds=random.randint(0, 300))

    return {
        "patient_id": patient_id,
        "timestamp": timestamp.isoformat() + "Z",
        "heart_rate": heart_rate,
        "temperature": temperature,
        "blood_pressure_systolic": systolic,
        "blood_pressure_diastolic": diastolic
    }

def simulate_streaming_data(num_records: int = 10, interval: float = 1.0):
    """Simulate streaming data by generating and appending records to Bronze layer."""
    try:
        logger.info(f"Starting streaming simulation for {num_records} records")

        base_timestamp = datetime.now()

        for i in range(num_records):
            # Generate data for a random patient
            patient_id = random.randint(1, 10)
            record = generate_vital_data(patient_id, base_timestamp)

            # Create DataFrame and append to Bronze CSV
            df = pd.DataFrame([record])
            output_path = f"{BRONZE_DIR}/streaming_healthcare_data.csv"

            # Append mode
            df.to_csv(output_path, mode='a', header=not pd.io.common.file_exists(output_path), index=False)
            logger.info(f"Appended streaming record: {record}")

            time.sleep(interval)  # Simulate real-time interval

        logger.info("Streaming simulation completed")

    except Exception as e:
        logger.error(f"Error in streaming simulation: {str(e)}")
        raise

if __name__ == "__main__":
    simulate_streaming_data()