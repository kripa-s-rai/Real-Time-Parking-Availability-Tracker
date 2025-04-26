from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType
import time

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RealTimeParkingTracker") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

# Define schema for incoming data
schema = StructType() \
    .add("lot_id", StringType()) \
    .add("status", StringType()) \
    .add("timestamp", StringType()) \
    .add("source", StringType())

# Start timer for streaming mode
start_time_streaming = time.time()

# Read from multiple Kafka topics streams
streams = []
for topic in ['sensor-topic', 'app-topic', 'external-topic']:
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .load() \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    streams.append(df)

# Union all streams into one DataFrame
stream_df = streams[0].union(streams[1]).union(streams[2])

# Convert the timestamp from string to TimestampType
stream_df = stream_df.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Apply windowing and aggregation (5-minute window)
windowed = stream_df.groupBy(
    window(col("timestamp"), "5 minutes"),  # Window size is 5 minutes
    col("lot_id")
).count()

# Extract window_start and window_end from the window column
windowed = windowed.withColumn("window_start", col("window.start")) \
                   .withColumn("window_end", col("window.end")) \
                   .drop("window")


# Define the function to write output to MySQL
def write_to_mysql(batch_df, batch_id):
    batch_df.write.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/parking") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "parking_log") \
        .option("user", "root") \
        .option("password", "Kripa@123") \
        .mode("append") \
        .save()

# Start the stream processing query with timeout (10 minutes)
query = windowed.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_mysql) \
    .start()

# Wait for termination with a timeout of 10 minutes (600 seconds)
query.awaitTermination(600)  # Stops after 10 minutes

# End timer and calculate streaming execution time
end_time_streaming = time.time()
streaming_execution_time = end_time_streaming - start_time_streaming
print(f"Streaming Mode Execution Time: {streaming_execution_time} seconds")

# Stop the stream query after completion
query.stop()

