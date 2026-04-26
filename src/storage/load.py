"""
Data storage module.
Loads processed Gold data into SQLite database with schema and example queries.
"""

import sqlite3
import pandas as pd
from src.utils.config import GOLD_DIR, DB_PATH
from src.utils.logging import get_logger

logger = get_logger(__name__)

def create_table_if_not_exists(conn: sqlite3.Connection, table_name: str):
    """Create healthcare_gold table if it doesn't exist."""
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        patient_id INTEGER PRIMARY KEY,
        avg_heart_rate REAL,
        avg_temperature REAL,
        avg_bp_systolic REAL,
        avg_bp_diastolic REAL,
        abnormal_count INTEGER
    );
    """
    conn.execute(create_table_sql)
    conn.commit()

def load_gold_to_db(layer: str = "batch"):
    """Load Gold layer data into SQLite database."""
    try:
        logger.info(f"Starting data load for {layer}")

        # Read Gold data
        gold_path = f"{GOLD_DIR}/{layer}_healthcare_data.csv"
        df = pd.read_csv(gold_path)
        logger.info(f"Read Gold data from {gold_path}")

        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)
        table_name = f"{layer}_healthcare_gold"

        # Create table
        create_table_if_not_exists(conn, table_name)

        # Load data
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logger.info(f"Data loaded into table {table_name}")

        # Example queries
        logger.info("Running example queries...")
        cursor = conn.cursor()

        # Query 1: Patients with high abnormal counts
        cursor.execute(f"SELECT patient_id, abnormal_count FROM {table_name} WHERE abnormal_count > 0 ORDER BY abnormal_count DESC")
        high_abnormal = cursor.fetchall()
        logger.info(f"Patients with abnormalities: {high_abnormal}")

        # Query 2: Average heart rate across all patients
        cursor.execute(f"SELECT AVG(avg_heart_rate) as overall_avg_hr FROM {table_name}")
        avg_hr = cursor.fetchone()[0]
        logger.info(f"Overall average heart rate: {avg_hr:.2f}")

        conn.close()
        logger.info("Data load and queries completed")

    except Exception as e:
        logger.error(f"Error in data load: {str(e)}")
        raise

if __name__ == "__main__":
    load_gold_to_db("batch")
