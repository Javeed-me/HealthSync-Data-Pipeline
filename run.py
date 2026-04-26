"""
Entry point for the healthcare data engineering project.
Provides a CLI to execute batch ingestion, streaming simulation, processing, and loading.
"""

import argparse
import sys
from src.ingestion.batch_ingest import ingest_batch_data
from src.ingestion.stream_simulate import simulate_streaming_data
from src.ingestion.generate_data import generate_patient_data, save_to_csv
from src.processing.transform import process_data
from src.storage.load import load_gold_to_db
from src.utils.config import BRONZE_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the healthcare data engineering pipelines")
    parser.add_argument(
        "command",
        choices=["batch-ingest", "stream-simulate", "batch-process", "stream-process", "load-db", "generate-data"],
        help="Pipeline command to run"
    )
    parser.add_argument(
        "--type",
        choices=["batch", "streaming"],
        default="batch",
        help="Data type for load-db command (default: batch)"
    )
    parser.add_argument(
        "--large",
        action="store_true",
        help="Use large generated dataset for batch-ingest (requires generate-data first)"
    )
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
        help="Output filename for generated data (default: healthcare_large.csv)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "generate-data":
        df = generate_patient_data(args.records)
        save_to_csv(df, args.output)
        print(f"OK Generated {len(df)} records -> data/input/{args.output}")
    elif args.command == "batch-ingest":
        ingest_batch_data(use_large=args.large)
    elif args.command == "stream-simulate":
        simulate_streaming_data()
    elif args.command == "batch-process":
        input_path = f"{BRONZE_DIR}/batch_healthcare_data.csv"
        process_data(input_path, layer="batch")
    elif args.command == "stream-process":
        input_path = f"{BRONZE_DIR}/streaming_healthcare_data.csv"
        process_data(input_path, layer="streaming")
    elif args.command == "load-db":
        load_gold_to_db(args.type)
    else:
        logger.error("Unknown command")
        sys.exit(1)

if __name__ == "__main__":
    main()
