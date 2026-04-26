"""
Unit tests for data quality functions.
"""

import pytest
import pandas as pd
from src.processing.quality import check_nulls, check_schema, check_duplicates

@pytest.fixture
def sample_df():
    data = {
        "patient_id": [1, 2, 3],
        "timestamp": ["2023-01-01T10:00:00Z", "2023-01-01T11:00:00Z", "2023-01-01T12:00:00Z"],
        "heart_rate": [70, 85, 200],
        "temperature": [36.5, 37.0, 42.5],
        "blood_pressure_systolic": [120, 130, 140],
        "blood_pressure_diastolic": [80, 85, 90]
    }
    return pd.DataFrame(data)

def test_check_schema(sample_df):
    expected_columns = ["patient_id", "timestamp", "heart_rate", "temperature", "blood_pressure_systolic", "blood_pressure_diastolic"]
    assert check_schema(sample_df, expected_columns)

def test_check_nulls_no_nulls(sample_df):
    assert check_nulls(sample_df, ["patient_id", "heart_rate", "temperature"])

def test_check_duplicates_unique(sample_df):
    assert check_duplicates(sample_df, ["patient_id", "timestamp"])