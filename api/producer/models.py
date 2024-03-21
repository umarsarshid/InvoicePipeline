from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Item(BaseModel):
    item_id: str
    description: str
    quantity: int
    price: float

class Invoice(BaseModel):
    invoice_id: str = Field(..., alias='id')
    customer_id: str
    gender: str
    age: int
    items: List[Item] = []  # Assuming multiple items can be under the same invoice
    payment_method: str
    date: str
    totalPrice: float

    class Config:
        schema_extra = {
            "example": {
                "id": "123456",
                "customer_id": "C12345",
                "gender": "Male",
                "age": 30,
                "items": [
                    {
                        "item_id": "item001",
                        "description": "Smartphone",
                        "quantity": 1,
                        "price": 999.99
                    }
                ],
                "payment_method": "Credit Card",
                "date": "2024-03-12",
                "totalPrice": 59.99
            }
        }
