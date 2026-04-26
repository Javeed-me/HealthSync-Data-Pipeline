# Check local environment for Spark and Kafka
Write-Host "Checking Python version..."
python --version

Write-Host "Checking Java installation..."
java -version

Write-Host "Checking SPARK_HOME..."
if ($env:SPARK_HOME) {
    Write-Host "SPARK_HOME is set to $env:SPARK_HOME"
} else {
    Write-Host "SPARK_HOME is not set. Set it to your Spark installation directory."
}

Write-Host "Checking Kafka command availability..."
if (Get-Command kafka-topics.cmd -ErrorAction SilentlyContinue) {
    Write-Host "Kafka commands are available."
} else {
    Write-Host "Kafka commands are not available in PATH."
}
