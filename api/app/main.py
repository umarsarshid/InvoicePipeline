from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from kafka import KafkaProducer
import json
from models import Invoice  # Importing the Invoice model


app = FastAPI()

class Invoice(BaseModel):
    id: str
    date: str
    customer_id: str
    items: list
    total: float

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

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