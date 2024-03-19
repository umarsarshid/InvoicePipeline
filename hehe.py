import requests
import json
import pandas as pd

# Endpoint URL of your FastAPI application
url = "http://0.0.0.0:8000/invoices/"

# Sample data to send
# Adjust this dictionary to match the schema expected by your FastAPI endpoint
# Load the CSV data
csv_file_path = 'customer_shopping_data.csv'
data = pd.read_csv(csv_file_path)

# Add a unique item ID for each category (enumerate starting from 1)
data['item_id'] = data.groupby('category').ngroup() + 1

# Transform data to match the expected structure
def transform_row(row):
    return {
        "id": row['invoice_no'],
        "date": str(row['invoice_date']),
        "customer_id": row['customer_id'],
        "items": [{
            "item_id": str(row['item_id']),
            "description": row['category'],
            "quantity": row['quantity'],
            "price_per_unit": row['price']
        }],
        "totalPrice": row['quantity'] * row['price'],
        "payment_method": row['payment_method'],
        "shopping_mall": row['shopping_mall'],
        "gender": row['gender'],
        "age": row['age']
    }
# Convert the dictionary to a JSON string
# data_json = json.dumps(data)

# Specify content type
# Iterate over each row and send the data
for _, row in data.iterrows():
    invoice_data = transform_row(row)
    response = requests.post(url, json=invoice_data)
    if response.status_code == 200:
        print("Invoice data sent successfully:", invoice_data)
    else:
        print("Failed to send invoice data:", response.text)
