from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
from models import Invoice  # Assuming this is your custom model import
import time

app = FastAPI()

class Invoice(BaseModel):
    id: str
    date: str
    customer_id: str
    items: list
    total: float

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
        producer.send('invoices', value=invoice.dict())
        producer.flush()  # Ensure data is sent to Kafka
        return {"message": "Invoice data sent to Kafka successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
