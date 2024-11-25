from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_spark_session():
    return SparkSession.builder \
        .appName("SEO Analysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
        .getOrCreate()

def process_seo_data():
    spark = create_spark_session()

    # Define schema for the data
    schema = StructType([
        StructField("url", StringType()),
        StructField("title", StringType()),
        StructField("viewport", StringType()),
        # Add other fields as needed
    ])

    # Read from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "seo_data") \
        .load()

    # Parse JSON data
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # Add processing timestamp
    processed_df = parsed_df.withColumn("processing_time", current_timestamp())

    # Write to PostgreSQL
    query = processed_df \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_seo_data()
