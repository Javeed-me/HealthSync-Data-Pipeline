---
# 🏥 Healthcare Data Engineering Platform

This project was developed as an extension of a patient diagnosis system to improve data quality, organization, and reliability for better clinical analysis and decision support.

It processes healthcare data from multiple sources, ensures data validation, detects abnormal patient conditions, and makes the data analytics-ready through a structured pipeline.
---
## 🎯 Problem Statement

In healthcare systems, patient data often comes from multiple sources such as medical records and monitoring devices. This data is frequently inconsistent, unstructured, and difficult to analyze.

To support effective patient diagnosis and decision-making, there is a need for a system that:

* Cleans and validates healthcare data
* Ensures consistency and reliability
* Detects abnormal patient conditions
* Provides structured, analytics-ready data

This project addresses these challenges by building a scalable data pipeline with validation, alerting, and visualization capabilities.

---

## 🚀 Key Features

* 🧱 Medallion Architecture (Bronze → Silver → Gold)
* 🔄 Batch & Simulated Streaming Pipelines
* 🧪 Data Quality Validation (nulls, duplicates, schema)
* 🚨 Healthcare Alerts (abnormal vitals detection)
* 📊 Interactive Dashboard (Streamlit)
* 📈 Synthetic Data Generation (scalable datasets)
* ⚙️ CLI-based pipeline execution
* 🧪 Unit Testing with pytest
* ☁️ Cloud-ready architecture (Azure mapping)

---

## 🧭 Architecture

### Medallion Architecture

| Layer            | Description                      |
| ---------------- | -------------------------------- |
| **Bronze** | Raw healthcare data              |
| **Silver** | Cleaned & validated data         |
| **Gold**   | Aggregated, analytics-ready data |

### Data Flow

```
CSV / Generator → Bronze → Silver → Gold → SQLite → Dashboard
```

---

## 🗂️ Project Structure

```
├── src/
│   ├── ingestion/          # Batch & streaming ingestion
│   ├── processing/         # Transformations & validations
│   ├── storage/            # Database loading
│   └── utils/              # Config & logging
├── tests/                  # Unit tests
├── data/                   # Bronze, Silver, Gold layers
├── dashboard/              # Streamlit app
├── run.py                  # CLI entry point
└── README.md
```

---

## ⚙️ Tech Stack

| Category        | Technology     | Purpose             |
| --------------- | -------------- | ------------------- |
| Language        | Python         | Core development    |
| Data Processing | Pandas         | Data transformation |
| Database        | SQLite         | Store final data    |
| Visualization   | Streamlit      | Dashboard UI        |
| Charts          | Matplotlib     | Graphs & insights   |
| Testing         | pytest         | Unit testing        |
| DevOps          | GitHub Actions | CI/CD               |

---

## ▶️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📊 Generate Data (Optional but Recommended)

```bash
python run.py generate-data --records 1000
```

---

## 🔄 Run Batch Pipeline

```bash
# Ingest data
python run.py batch-ingest

# Process data
python run.py batch-process

# Load into database
python run.py load-db --type batch
```

---

## ⚡ Run Streaming Pipeline

```bash
python run.py stream-simulate
python run.py stream-process
python run.py load-db --type streaming
```

---

## 📊 Run Dashboard

```bash
streamlit run dashboard/app.py
```

Then open:
👉 [http://localhost:8501](http://localhost:8501/)

---

## 🧠 Healthcare Validations

| Metric      | Normal Range |
| ----------- | ------------ |
| Heart Rate  | 40–180 bpm  |
| Temperature | 35–42 °C   |

👉 Abnormal values are flagged and shown in dashboard alerts.

---

## 🗄️ Database

SQLite database:

```
data/healthcare_gold.db
```

Tables:

* `batch_healthcare_gold`
* `streaming_healthcare_gold`

---

## 📊 Dashboard Features

* Key metrics (patients, alerts, vitals)
* Abnormal patient detection
* Interactive charts:
  * Heart rate trends
  * Temperature analysis
  * Alert distribution
* Full dataset viewer

---

## 📈 Scaling with Synthetic Data

To simulate real-world scenarios:

```bash
python run.py generate-data --records 10000
```

This allows:

* Testing pipeline performance
* Demonstrating scalability
* Generating realistic datasets

---

## ☁️ Future Enhancements (Azure Mapping)

| Current          | Azure Equivalent           |
| ---------------- | -------------------------- |
| Pandas           | Azure Databricks (PySpark) |
| CSV Files        | Azure Data Lake            |
| SQLite           | Azure SQL Database         |
| Python Streaming | Azure Event Hub            |
| CLI Scripts      | Azure Data Factory         |

---

## 🧪 Testing

Run tests:

```bash
pytest tests/
```

✔ Ensures:

* Data quality checks
* Transformations
* Pipeline reliability

---

## 🏆 Key Highlights

* End-to-end data pipeline
* Real-world healthcare use case
* Scalable architecture design
* Production-like structure
* Visualization + analytics

---

## 💡 Future Improvements

* Cloud deployment on Azure
* Real-time streaming with Kafka/Event Hub
* Distributed processing with Spark
* Advanced anomaly detection
* API-based data ingestion
