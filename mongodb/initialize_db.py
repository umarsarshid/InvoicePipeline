from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = 'mongodb://mongodb:27017/'

# Name of our database
DB_NAME = 'ecommerce'

# Collection names
COLLECTION_NAMES = ['invoices', 'customers']

# Establishing a connection to MongoDB
client = MongoClient(MONGO_URI, username = 'root', password = 'example')

# Creating a database
db = client[DB_NAME]

def create_collections_and_indexes():
    for collection_name in COLLECTION_NAMES:
        # Create collection if it doesn't already exist
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection {collection_name} already exists.")
        
        # Example: Creating an index on the 'customer_id' field of the 'invoices' collection
        if collection_name == 'invoices':
            db[collection_name].create_index([('customer_id', 1)])
            print(f"Index created on {collection_name}.customer_id")

if __name__ == '__main__':
    create_collections_and_indexes()
