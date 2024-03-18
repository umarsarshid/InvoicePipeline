from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import pandas as pd
import plotly.express as px

# MongoDB connection URI
MONGO_URI = 'mongodb://localhost:27017/'

try:
    
    client = MongoClient(MONGO_URI, username = 'root', password = 'example')
    # Force a call to the server to test connection
    client.admin.command('ping')
    print("Connected successfully to MongoDB")
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    exit(1)

def list_databases_and_collections():
    # List all databases
    databases = client.list_database_names()
    
    for db_name in databases:
        # Skip system databases
        if db_name in ["admin", "local", "config"]:
            continue
        
        print(f"Database: {db_name}")
        
        # Access the database
        db = client[db_name]
        
        # List all collections in the database
        collections = db.list_collection_names()
        for collection_name in collections:
            print(f"  Collection: {collection_name}")
            
            # Access the collection
            collection = db[collection_name]
            
            # Optionally, get a count of documents in the collection
            count_documents = collection.count_documents({})
            print(f"    Document Count: {count_documents}")
            
            # Optionally, display the first document as an example
            first_document = collection.find_one()
            print(f"    First Document: {first_document}")
            
def func():
    db = client.ecommerce
    collection = db.invoices
    
    print

    pipeline = [
        {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}  # Sort by date ascending
    ]

    invoices_by_date = list(collection.aggregate(pipeline))
    print(invoices_by_date)

    # Convert to DataFrame
    df = pd.DataFrame(invoices_by_date)
    print(df)
    # df.rename(columns={'_id': 'Date', 'count': 'Number of Invoices'}, inplace=True)
    # df['Date'] = pd.to_datetime(df['Date']).dt.date  # Ensure 'Date' is in date format

    # fig = px.bar(df, x='Date', y='Number of Invoices', title='Invoices by Date')



if __name__ == '__main__':
    # list_databases_and_collections()
    func()
