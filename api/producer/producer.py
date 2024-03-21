from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
from models import Invoice  # Assuming this is your custom model import
import time
from pymongo import MongoClient, errors as mongo_errors
import logging
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
try:
    client = MongoClient('mongodb://mongodb:27017/', username='root', password='example')
    db = client.ecommerce
    collection = db.invoices
    logger.info("Connected to MongoDB")
except mongo_errors.ConnectionFailure as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    exit(1)

class Invoice(BaseModel):
    id: str
    customer_id: str
    gender: str
    age: int # Assuming each invoice has a single category for simplification
    items: list
    payment_method: str
    date: str
    totalPrice: float
    
def get_kafka_producer(attempts=5, wait=5):
    for _ in range(attempts):
        try:
            producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'), 
                                     api_version=(2, 0, 2))
            print("Connected to Kafka!")
            return producer
        except NoBrokersAvailable:
            print(f"Waiting for Kafka to become available. Retrying in {wait} seconds...")
            time.sleep(wait)
    raise Exception("Failed to connect to Kafka after several attempts.")

# Initialize Kafka producer with retry mechanism
producer = get_kafka_producer()

@app.post("/invoices/")
async def post_invoice(invoice: Invoice):
    """
    Receives invoice data and sends it to a Kafka topic.
    """
    try:
        # Send invoice data to Kafka topic 'invoices'
        # print(invoice.dict())
        producer.send('invoices', value=invoice.dict())
        producer.flush()  # Ensure data is sent to Kafka
        return {"message": "Invoice data sent to Kafka successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/top_performing_products/")
async def top_performing_products():
   pipeline = [
        # Unwind the items array to treat each item as a separate document
        {"$unwind": "$items"},
        # Group by item description
        {
            "$group": {
                "_id": {
                    "description": "$items.description",
                },
                # Sum up the totalPrice for each item
                "total_sales": {"$sum": "$totalPrice"}
            }
        },
        # Sort the results by total_sales in descending order
        {"$sort": {"total_sales": -1}}
        ]
   results = list(collection.aggregate(pipeline))
   print(results)
   return results

@app.get("/sales_trends/")
async def sales_trends():
    pipeline = [
        # Convert 'date' to a date object
        {"$addFields": {"dateObj": {"$dateFromString": {"dateString": "$date", "format": "%m/%d/%Y"}}}},
        # Group by day
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$dateObj"},
                    "month": {"$month": "$dateObj"},
                    "day": {"$dayOfMonth": "$dateObj"},
                },
                "daily_sales": {"$sum": "$totalPrice"},
                "transactions": {"$sum": 1}
            }
        },
        # Sort by date ascending
        {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
    ]
    results = list(collection.aggregate(pipeline))
    # Convert MongoDB objects to JSON serializable format
    return json.loads(dumps(results))