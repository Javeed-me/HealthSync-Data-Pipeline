"""
Kafka consumer for streaming data.
Consumes messages from Kafka topic and processes them.
"""

import json
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from src.utils.config import BRONZE_DIR, KAFKA_TOPIC, KAFKA_SERVERS, SPARK_APP_NAME
from src.utils.logging import get_logger

logger = get_logger(__name__)

def consume_streaming_data():
    """Consume streaming data from Kafka and store in Bronze layer."""
    try:
        logger.info("Starting Kafka consumer")

        # Initialize Spark session
        spark = SparkSession.builder.appName(SPARK_APP_NAME).getOrCreate()

        # Initialize Kafka consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='data_group',
            consumer_timeout_ms=10000
        )

        messages = []
        # Consume messages until there are no new records or a timeout occurs
        for message in consumer:
            data = message.value
            messages.append(data)
            logger.info(f"Consumed message: {data}")

            if len(messages) >= 5:  # Adjust maximum batch size as needed
                break

        if messages:
            # Create DataFrame from messages
            df = spark.createDataFrame(messages)
            output_path = f"{BRONZE_DIR}/streaming_data"
            df.write.mode("overwrite").parquet(output_path)
            logger.info(f"Streaming data written to Bronze at {output_path}")
        else:
            logger.warning("No messages consumed")

        consumer.close()
        spark.stop()
        logger.info("Kafka consumer completed")

    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}")
        raise

if __name__ == "__main__":
    consume_streaming_data()