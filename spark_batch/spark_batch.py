from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window
import time

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ParkingTrackerBatch") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

# Start timer for batch mode
start_time_batch = time.time()

# Read data from MySQL (this is where data is saved by the streaming job)
batch_df = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/parking") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "parking_log") \
    .option("user", "root") \
    .option("password", "Kripa@123") \
    .load()

# Convert 'window_start' to timestamp (if not already in timestamp format)
batch_df = batch_df.withColumn("window_start", col("window_start").cast("timestamp"))

# Apply windowing and aggregation (using 'window_start' instead of 'timestamp')
windowed_batch = batch_df.groupBy(
    window(col("window_start"), "5 minutes"),  # 5-minute window aggregation
    col("lot_id")
).count()

# Rename the count column to 'event_count'
windowed_batch = windowed_batch.withColumnRenamed("count", "event_count")

# Extract 'window_start' and 'window_end' from the 'window' column
windowed_batch = windowed_batch.withColumn("window_start", col("window.start")) \
                               .withColumn("window_end", col("window.end"))

# Drop the original 'window' column
windowed_batch = windowed_batch.drop("window")

# Ensure 'lot_id' is of IntegerType to match the database schema
windowed_batch = windowed_batch.withColumn("lot_id", col("lot_id").cast("string"))

# Write the result to MySQL (you may use a different table for batch results)
windowed_batch.write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/parking") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "parking_log_batch") \
    .option("user", "root") \
    .option("password", "Kripa@123") \
    .mode("append") \
    .save()

# End timer and calculate batch execution time
end_time_batch = time.time()
batch_execution_time = end_time_batch - start_time_batch
print(f"Batch Mode Execution Time: {batch_execution_time} seconds")


