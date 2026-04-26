"""
Unit tests for Pandas transformation logic.
"""

import pytest
import pandas as pd
import os
from src.processing.transform import bronze_to_silver, silver_to_gold
from src.processing.quality import validate_data_quality
from src.utils.config import BRONZE_DIR

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

def test_validate_data_quality(sample_df):
    assert validate_data_quality(sample_df)

def test_bronze_to_silver(sample_df):
    # Save to temp file
    temp_path = f"{BRONZE_DIR}/test_data.csv"
    sample_df.to_csv(temp_path, index=False)
    
    df_silver = bronze_to_silver(temp_path)
    assert 'heart_rate_abnormal' in df_silver.columns
    assert 'any_abnormal' in df_silver.columns
    
    # Clean up
    os.remove(temp_path)

def test_bronze_to_silver_flags_generated_oxygen_saturation(sample_df):
    sample_df["oxygen_saturation"] = [98, 94, 99]
    temp_path = f"{BRONZE_DIR}/test_oxygen_data.csv"
    sample_df.to_csv(temp_path, index=False)

    df_silver = bronze_to_silver(temp_path)
    assert 'oxygen_saturation_abnormal' in df_silver.columns
    assert df_silver.loc[1, 'oxygen_saturation_abnormal']
    assert df_silver.loc[1, 'any_abnormal']

    os.remove(temp_path)

def test_silver_to_gold(sample_df):
    # Mock silver df with flags
    sample_df['heart_rate_abnormal'] = [False, False, True]
    sample_df['temperature_abnormal'] = [False, False, True]
    sample_df['any_abnormal'] = [False, False, True]
    
    df_gold = silver_to_gold(sample_df)
    assert len(df_gold) == 3  # One per patient
    assert 'avg_heart_rate' in df_gold.columns
    assert 'abnormal_count' in df_gold.columns
