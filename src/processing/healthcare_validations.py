"""
Healthcare-specific validation functions.
Checks vital signs against medical ranges and flags abnormalities.
"""

import pandas as pd
from src.utils.config import HEART_RATE_MIN, HEART_RATE_MAX, TEMPERATURE_MIN, TEMPERATURE_MAX, OXYGEN_SATURATION_MIN
from src.utils.logging import get_logger

logger = get_logger(__name__)

def validate_heart_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Validate heart rate and flag abnormalities."""
    df = df.copy()
    df['heart_rate_abnormal'] = (df['heart_rate'] < HEART_RATE_MIN) | (df['heart_rate'] > HEART_RATE_MAX)
    abnormal_count = df['heart_rate_abnormal'].sum()
    if abnormal_count > 0:
        logger.warning(f"Found {abnormal_count} abnormal heart rate records")
    return df

def validate_temperature(df: pd.DataFrame) -> pd.DataFrame:
    """Validate temperature and flag abnormalities."""
    df = df.copy()
    df['temperature_abnormal'] = (df['temperature'] < TEMPERATURE_MIN) | (df['temperature'] > TEMPERATURE_MAX)
    abnormal_count = df['temperature_abnormal'].sum()
    if abnormal_count > 0:
        logger.warning(f"Found {abnormal_count} abnormal temperature records")
    return df

def validate_oxygen_saturation(df: pd.DataFrame) -> pd.DataFrame:
    """Validate oxygen saturation when the field is present."""
    df = df.copy()
    if 'oxygen_saturation' not in df.columns:
        df['oxygen_saturation_abnormal'] = False
        return df

    df['oxygen_saturation_abnormal'] = df['oxygen_saturation'] < OXYGEN_SATURATION_MIN
    abnormal_count = df['oxygen_saturation_abnormal'].sum()
    if abnormal_count > 0:
        logger.warning(f"Found {abnormal_count} abnormal oxygen saturation records")
    return df

def flag_abnormal_vitals(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all healthcare validations and flag any abnormalities."""
    df = validate_heart_rate(df)
    df = validate_temperature(df)
    df = validate_oxygen_saturation(df)
    df['any_abnormal'] = (
        df['heart_rate_abnormal']
        | df['temperature_abnormal']
        | df['oxygen_saturation_abnormal']
    )
    logger.info(f"Flagged {df['any_abnormal'].sum()} records with abnormalities")
    return df
