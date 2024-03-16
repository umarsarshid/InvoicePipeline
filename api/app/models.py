# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Item(BaseModel):
    item_id: str
    description: str
    quantity: int
    price_per_unit: float

class Invoice(BaseModel):
    invoice_id: str = Field(..., alias='id')
    date: str
    customer_id: str
    items: List[Item]
    total: Optional[float] = None

    class Config:
        schema_extra = {
                "id": "12345",
                "date": "2024-03-12",
                "customer_id": "cust001",
                "items": [
                    {
                        "item_id": "item001",
                        "description": "Wireless Mouse",
                        "quantity": 2,
                        "price_per_unit": 29.99
                    }
                ],
                "total": 59.98
        }