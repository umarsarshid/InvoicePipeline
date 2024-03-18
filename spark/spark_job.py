from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType, ArrayType, StructField

def main():
    # Define schema of invoice data based on the models.py you have
    invoiceSchema = StructType([
        StructField("invoice_id", StringType()),
        StructField("date", StringType()),
        StructField("customer_id", StringType()),
        StructField("items", ArrayType(StructType([
            StructField("item_id", StringType()),
            StructField("description", StringType()),
            StructField("quantity", IntegerType()),
            StructField("price_per_unit", FloatType())
        ]))),
        StructField("totaPrice", FloatType())
    ])

    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("Spark Streaming from Kafka to MongoDB") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/invoicedb.processed_invoices") \
        .getOrCreate()

    # Read from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "invoices") \
        .load()

    # Deserialize JSON from Kafka
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), invoiceSchema).alias("data")) \
        .select("data.*")

    # Process data (this example simply forwards the data, but you can add transformations)

    # Write the results to MongoDB
    query = df.writeStream \
        .format("mongo") \
        .option("checkpointLocation", "/path/to/checkpoint/dir") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
