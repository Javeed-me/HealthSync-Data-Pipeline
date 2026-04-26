"""
Data quality validation functions using Pandas.
"""

import pandas as pd
from src.utils.logging import get_logger

logger = get_logger(__name__)

def check_nulls(df: pd.DataFrame, columns: list) -> bool:
    """Check for null values in specified columns."""
    null_counts = df[columns].isnull().sum()
    has_nulls = null_counts.sum() > 0
    if has_nulls:
        logger.warning(f"Null values found: {null_counts.to_dict()}")
    return not has_nulls

def check_duplicates(df: pd.DataFrame, columns: list) -> bool:
    """Check for duplicates based on specified columns."""
    dup_count = df.duplicated(subset=columns).sum()
    if dup_count > 0:
        logger.warning(f"Duplicates found: {dup_count} duplicate records")
        return False
    return True

def check_schema(df: pd.DataFrame, expected_columns: list) -> bool:
    """Check if DataFrame has expected columns (allows extra columns)."""
    actual_columns = list(df.columns)
    missing_columns = set(expected_columns) - set(actual_columns)
    if missing_columns:
        logger.error(f"Schema mismatch. Missing columns: {missing_columns}")
        return False
    return True

def validate_data_quality(df: pd.DataFrame) -> bool:
    """Run all quality checks."""
    expected_columns = ["patient_id", "timestamp", "heart_rate", "temperature", "blood_pressure_systolic", "blood_pressure_diastolic"]
    columns = ["patient_id", "heart_rate", "temperature"]

    schema_ok = check_schema(df, expected_columns)
    nulls_ok = check_nulls(df, columns)
    dups_ok = check_duplicates(df, ["patient_id", "timestamp"])  # Assume unique per patient-timestamp

    return schema_ok and nulls_ok and dups_ok