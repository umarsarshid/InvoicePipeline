from kafka import KafkaConsumer
from kafka.errors import KafkaError
from pymongo import MongoClient, errors as mongo_errors
import json
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka Consumer Configuration
consumer = KafkaConsumer('invoices',
                         bootstrap_servers=['kafka:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         api_version=(2, 0, 2),
                         group_id='my_group',
                         auto_offset_reset='earliest',  # Start reading at the earliest message
                         enable_auto_commit=False)  # Manual commit of offsets

# MongoDB Connection
try:
    client = MongoClient('mongodb://mongodb:27017/', username='root', password='example')
    db = client.ecommerce
    collection = db.invoices
    logger.info("Connected to MongoDB")
except mongo_errors.ConnectionFailure as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    exit(1)

# Consume Messages from Kafka and Store Them in MongoDB
try:
    for message in consumer:
        invoice_data = message.value
        try:
            # Attempt to insert document into MongoDB
            collection.insert_one(invoice_data)
            logger.info(f"Inserted invoice into MongoDB: {invoice_data}")
            consumer.commit()  # Commit the offset after successful insertion
        except mongo_errors.PyMongoError as e:
            logger.error(f"Failed to insert document into MongoDB: {e}")
            # Handle MongoDB insertion error (e.g., retry, log, alert)
except KafkaError as e:
    logger.error(f"Error consuming messages from Kafka: {e}")
    # Handle Kafka consumer error (e.g., retry, log, alert)
finally:
    consumer.close()
