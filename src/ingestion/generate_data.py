"""
Synthetic data generation module for healthcare pipeline.
Generates realistic healthcare patient data with configurable record counts.
Supports generating 1000, 5000, 10000+ records for scalability testing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import argparse

# Add project root to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.config import DATA_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)

# Configuration
OUTPUT_DIR = os.path.join(DATA_DIR, "input")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Healthcare validation ranges (for generating realistic data)
HEART_RATE_MIN = 40
HEART_RATE_MAX = 180
TEMPERATURE_MIN = 35.0
TEMPERATURE_MAX = 42.0
SYSTOLIC_MIN = 80
SYSTOLIC_MAX = 200
DIASTOLIC_MIN = 50
DIASTOLIC_MAX = 130


def generate_patient_id(index: int) -> str:
    """Generate unique patient ID."""
    return f"P{str(index).zfill(6)}"


def generate_timestamp(base_time: datetime, offset_minutes: int = 0) -> str:
    """Generate timestamp with optional offset."""
    return (base_time + timedelta(minutes=offset_minutes)).strftime("%Y-%m-%d %H:%M:%S")


def generate_normal_vitals(randomizer: np.random.Generator) -> dict:
    """Generate normal vital signs (80% of patients)."""
    return {
        "heart_rate": randomizer.integers(60, 100),
        "temperature": round(randomizer.uniform(36.0, 37.5), 1),
        "systolic_bp": randomizer.integers(100, 130),
        "diastolic_bp": randomizer.integers(60, 85),
        "oxygen_saturation": randomizer.integers(95, 100),
    }


def generate_abnormal_vitals(randomizer: np.random.Generator) -> dict:
    """Generate abnormal vital signs (20% of patients)."""
    # Randomly choose type of abnormality
    abnormality_type = randomizer.integers(0, 4)
    
    if abnormality_type == 0:  # High heart rate (tachycardia)
        return {
            "heart_rate": randomizer.integers(181, 201),
            "temperature": round(randomizer.uniform(36.0, 37.5), 1),
            "systolic_bp": randomizer.integers(100, 130),
            "diastolic_bp": randomizer.integers(60, 85),
            "oxygen_saturation": randomizer.integers(95, 100),
        }
    elif abnormality_type == 1:  # Low heart rate (bradycardia)
        return {
            "heart_rate": randomizer.integers(30, 40),
            "temperature": round(randomizer.uniform(36.0, 37.5), 1),
            "systolic_bp": randomizer.integers(100, 130),
            "diastolic_bp": randomizer.integers(60, 85),
            "oxygen_saturation": randomizer.integers(95, 100),
        }
    elif abnormality_type == 2:  # High temperature (fever)
        return {
            "heart_rate": randomizer.integers(60, 100),
            "temperature": round(randomizer.uniform(42.1, 43.1), 1),
            "systolic_bp": randomizer.integers(100, 130),
            "diastolic_bp": randomizer.integers(60, 85),
            "oxygen_saturation": randomizer.integers(95, 100),
        }
    else:  # Low oxygen saturation (hypoxia)
        return {
            "heart_rate": randomizer.integers(60, 100),
            "temperature": round(randomizer.uniform(36.0, 37.5), 1),
            "systolic_bp": randomizer.integers(100, 130),
            "diastolic_bp": randomizer.integers(60, 85),
            "oxygen_saturation": randomizer.integers(85, 95),
        }


def generate_patient_data(num_records: int, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic healthcare patient data.
    
    Args:
        num_records: Number of patient records to generate
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with synthetic patient data
    """
    logger.info(f"Generating {num_records} synthetic patient records...")
    
    # Initialize random generator
    randomizer = np.random.default_rng(seed)
    
    # Base timestamp
    base_time = datetime.now() - timedelta(days=30)
    
    # Generate data
    records = []
    for i in range(num_records):
        patient_id = generate_patient_id(i + 1)
        timestamp = generate_timestamp(base_time, offset_minutes=i)
        
        # 80% normal, 20% abnormal
        is_abnormal = randomizer.random() < 0.2
        
        if is_abnormal:
            vitals = generate_abnormal_vitals(randomizer)
        else:
            vitals = generate_normal_vitals(randomizer)
        
        record = {
            "patient_id": patient_id,
            "timestamp": timestamp,
            "heart_rate": vitals["heart_rate"],
            "temperature": vitals["temperature"],
            "blood_pressure_systolic": vitals["systolic_bp"],
            "blood_pressure_diastolic": vitals["diastolic_bp"],
            "oxygen_saturation": vitals["oxygen_saturation"],
            "patient_name": f"Patient_{i+1}",
            "age": randomizer.integers(18, 90),
            "gender": randomizer.choice(["Male", "Female"]),
            "department": randomizer.choice(["Emergency", "ICU", "General Ward", "Cardiology"]),
        }
        
        records.append(record)
    
    df = pd.DataFrame(records)
    logger.info(f"Generated {len(df)} records with {len(df[df['heart_rate'] > 100] + df[df['heart_rate'] < 60] + df[df['temperature'] > 38] + df[df['oxygen_saturation'] < 95])} abnormal readings")
    
    return df


def save_to_csv(df: pd.DataFrame, filename: str = "healthcare_large.csv") -> str:
    """Save DataFrame to CSV in input directory."""
    output_path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path}")
    return output_path


def main():
    """CLI entry point for data generation."""
    parser = argparse.ArgumentParser(description="Generate synthetic healthcare data")
    parser.add_argument(
        "--records", 
        type=int, 
        default=1000,
        help="Number of records to generate (default: 1000)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="healthcare_large.csv",
        help="Output filename (default: healthcare_large.csv)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    
    args = parser.parse_args()
    
    # Generate data
    df = generate_patient_data(args.records, args.seed)
    
    # Save to CSV
    output_path = save_to_csv(df, args.output)
    
    print(f"\nOK Generated {len(df)} records")
    print(f"   Saved to: {output_path}")
    print(f"   Normal readings: ~80%")
    print(f"   Abnormal readings: ~20%")


if __name__ == "__main__":
    main()
