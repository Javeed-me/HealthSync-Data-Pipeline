#!/bin/bash
# Setup script for local Spark installation on Linux/Mac
# Note: For Windows, adapt to PowerShell or use WSL
# Requires Java 8+ installed

# Download Spark (adjust version as needed)
SPARK_VERSION=3.5.0
HADOOP_VERSION=3
wget https://downloads.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
tar -xzf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
mv spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION spark

# Set environment variables (add to ~/.bashrc or ~/.zshrc)
export SPARK_HOME=$(pwd)/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

echo "Spark setup complete. Set SPARK_HOME and PATH as above."