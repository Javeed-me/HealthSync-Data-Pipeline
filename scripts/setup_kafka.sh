#!/bin/bash
# Setup script for local Kafka installation on Linux/Mac
# Note: For Windows, adapt to PowerShell or use WSL

# Download Kafka (adjust version as needed)
KAFKA_VERSION=3.6.0
wget https://downloads.apache.org/kafka/$KAFKA_VERSION/kafka_2.13-$KAFKA_VERSION.tgz
tar -xzf kafka_2.13-$KAFKA_VERSION.tgz
mv kafka_2.13-$KAFKA_VERSION kafka

# Start Zookeeper
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties &
sleep 5

# Start Kafka
bin/kafka-server-start.sh config/server.properties &
sleep 5

echo "Kafka setup complete. Zookeeper and Kafka are running."