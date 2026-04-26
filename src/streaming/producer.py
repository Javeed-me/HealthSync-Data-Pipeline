"""
Kafka producer for streaming data simulation.
Sends mock data to Kafka topic to simulate real-time ingestion.
"""

import json
import time
import pandas as pd
from kafka import KafkaProducer
from src.utils.config import SAMPLE_CSV, KAFKA_TOPIC, KAFKA_SERVERS
from src.utils.logging import get_logger

logger = get_logger(__name__)

def produce_streaming_data():
    """Produce streaming data to Kafka topic."""
    try:
        logger.info("Starting Kafka producer")

        # Initialize Kafka producer
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Read sample data
        df = pd.read_csv(SAMPLE_CSV)
        logger.info(f"Loaded {len(df)} records for streaming")

        # Send each row as a message
        for index, row in df.iterrows():
            message = {
                "id": int(row["id"]),
                "name": row["name"],
                "value": float(row["value"]),
                "timestamp": row["timestamp"]
            }
            producer.send(KAFKA_TOPIC, value=message)
            logger.info(f"Sent message: {message}")
            time.sleep(1)  # Simulate real-time delay

        producer.flush()
        producer.close()
        logger.info("Kafka producer completed")

    except Exception as e:
        logger.error(f"Error in producer: {str(e)}")
        raise

if __name__ == "__main__":
    produce_streaming_data()