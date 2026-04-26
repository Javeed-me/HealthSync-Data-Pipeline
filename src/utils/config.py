"""
Configuration file for the healthcare data engineering project.
Centralized configuration for paths, database connections, etc.
"""

import os

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BRONZE_DIR = os.path.join(DATA_DIR, "bronze")
SILVER_DIR = os.path.join(DATA_DIR, "silver")
GOLD_DIR = os.path.join(DATA_DIR, "gold")

# Sample data
SAMPLE_CSV = os.path.join(DATA_DIR, "sample_healthcare.csv")
INPUT_DIR = os.path.join(DATA_DIR, "input")
LARGE_CSV = os.path.join(INPUT_DIR, "healthcare_large.csv")

# Database
DB_PATH = os.path.join(DATA_DIR, "healthcare_gold.db")  # SQLite database

# Logging
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "healthcare_app.log")

# Healthcare validation ranges
HEART_RATE_MIN = 40
HEART_RATE_MAX = 180
TEMPERATURE_MIN = 35.0
TEMPERATURE_MAX = 42.0
OXYGEN_SATURATION_MIN = 95
