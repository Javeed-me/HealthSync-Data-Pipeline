"""
Healthcare Monitoring Dashboard (Clean UI Version)
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import visualization functions
from visualizations import (
    plot_heart_rate_per_patient,
    plot_temperature_trends,
    plot_abnormal_distribution,
    plot_blood_pressure,
    plot_vitals_summary
)
from src.ingestion.batch_ingest import ingest_batch_data
from src.ingestion.generate_data import generate_patient_data, save_to_csv
from src.ingestion.stream_simulate import simulate_streaming_data
from src.processing.transform import process_data
from src.storage.load import load_gold_to_db
from src.utils.config import BRONZE_DIR, DB_PATH, LARGE_CSV

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Healthcare Monitoring Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ============================================================
# DATA LOADING
# ============================================================
def table_has_data(db_path: str, table_name: str) -> bool:
    if not os.path.exists(db_path):
        return False

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if cursor.fetchone() is None:
                return False

            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0] > 0
    except sqlite3.Error:
        return False


def run_batch_pipeline():
    if not os.path.exists(LARGE_CSV):
        df = generate_patient_data(1000)
        save_to_csv(df, "healthcare_large.csv")

    ingest_batch_data(use_large=True)
    process_data(os.path.join(BRONZE_DIR, "batch_healthcare_data.csv"), layer="batch")
    load_gold_to_db("batch")


def run_streaming_pipeline():
    simulate_streaming_data(num_records=10, interval=0)
    process_data(os.path.join(BRONZE_DIR, "streaming_healthcare_data.csv"), layer="streaming")
    load_gold_to_db("streaming")


def ensure_pipeline_data(table_name: str, data_type: str, force_refresh: bool = False):
    if not force_refresh and table_has_data(DB_PATH, table_name):
        return

    with st.spinner(f"Preparing {data_type} pipeline data..."):
        if data_type == "Batch Processing":
            run_batch_pipeline()
        else:
            run_streaming_pipeline()


def load_data_from_sqlite(db_path: str, table_name: str) -> pd.DataFrame:
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def get_data_source():
    st.sidebar.header("📊 Data Source")

    data_type = st.sidebar.radio(
        "Select data type:",
        ["Batch Processing", "Streaming Data"]
    )

    table_map = {
        "Batch Processing": "batch_healthcare_gold",
        "Streaming Data": "streaming_healthcare_gold"
    }

    return table_map[data_type], data_type


# ============================================================
# METRICS
# ============================================================
def display_metrics(df: pd.DataFrame):
    st.subheader("📊 Key Metrics")

    total_patients = len(df)
    patients_with_alerts = (df['abnormal_count'] > 0).sum()
    total_alerts = int(df['abnormal_count'].sum())
    avg_heart_rate = df['avg_heart_rate'].mean()
    avg_temperature = df['avg_temperature'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Patients", total_patients)
    col2.metric("Patients with Alerts", patients_with_alerts)
    col3.metric("Total Alerts", total_alerts)
    col4.metric("Avg Heart Rate", f"{avg_heart_rate:.1f} bpm")
    col5.metric("Avg Temperature", f"{avg_temperature:.1f} °C")


# ============================================================
# ALERTS
# ============================================================
def display_abnormal_patients(df: pd.DataFrame):
    st.subheader("🚨 Abnormal Patients")

    abnormal_df = df[df['abnormal_count'] > 0]

    if len(abnormal_df) > 0:
        st.error(f"{len(abnormal_df)} patient(s) with abnormal vitals detected")

        st.dataframe(
            abnormal_df,
            use_container_width=True
        )
    else:
        st.success("All patients are within normal range")


# ============================================================
# CHARTS
# ============================================================
def display_charts(df: pd.DataFrame):
    st.subheader("📈 Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Heart Rate per Patient")
        st.pyplot(plot_heart_rate_per_patient(df))

    with col2:
        st.write("Temperature Trends")
        st.pyplot(plot_temperature_trends(df))

    col3, col4 = st.columns(2)

    with col3:
        st.write("Abnormal Distribution")
        st.pyplot(plot_abnormal_distribution(df))

    with col4:
        st.write("Blood Pressure")
        st.pyplot(plot_blood_pressure(df))

    st.write("Vitals Summary")
    st.pyplot(plot_vitals_summary(df))


# ============================================================
# FULL DATASET
# ============================================================
def display_full_dataset(df: pd.DataFrame):
    st.subheader("📋 Full Dataset")
    st.dataframe(df, use_container_width=True)


# ============================================================
# MAIN APP
# ============================================================
def main():
    st.title("🏥 Healthcare Monitoring Dashboard")

    table_name, data_type = get_data_source()
    refresh_pipeline = st.sidebar.button("Run pipeline again")

    ensure_pipeline_data(table_name, data_type, force_refresh=refresh_pipeline)

    df = load_data_from_sqlite(DB_PATH, table_name)

    if df.empty:
        st.warning("No data available after running the pipeline.")
        return

    st.sidebar.markdown("---")
    st.sidebar.write(f"**Data Type:** {data_type}")
    st.sidebar.write(f"**Table:** {table_name}")

    display_metrics(df)

    st.divider()

    display_abnormal_patients(df)

    st.divider()

    display_charts(df)

    st.divider()

    with st.expander("📋 View Full Dataset"):
        display_full_dataset(df)

    st.markdown("---")
    st.caption("Healthcare Monitoring Dashboard • Medallion Architecture • SQLite")


if __name__ == "__main__":
    main()
