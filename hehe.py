import requests
import json

# Endpoint URL of your FastAPI application
url = "http://0.0.0.0:8000/invoices/"

# Sample data to send
# Adjust this dictionary to match the schema expected by your FastAPI endpoint
data = { 
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
    "totalPrice": 59.98
}

# Convert the dictionary to a JSON string
# data_json = json.dumps(data)

# Specify content type
headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(url, json=data)
# print(data_json)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response Text:", response.text)
