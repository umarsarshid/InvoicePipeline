import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# MongoDB connection setup
client = MongoClient('mongodb://mongodb:27017/', username='root', password='example')
db = client.ecommerce
collection = db.invoices

# Streamlit layout
st.title('Invoice Dashboard')
st.markdown('Explore invoice data from MongoDB.')

# Sidebar filters
customer_id = st.sidebar.selectbox('Select Customer ID', collection.distinct('customer_id'))
# Assume 'date' field exists and is of

# Aggregate invoices by date
pipeline = [
    {"$group": {"_id": "$date", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}  # Sort by date ascending
]

invoices_by_date = list(collection.aggregate(pipeline))
# print(invoices_by_date)

# Convert to DataFrame
df = pd.DataFrame(invoices_by_date)
# print(df)
df.rename(columns={'_id': 'Date', 'count': 'Number of Invoices'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date']).dt.date  # Ensure 'Date' is in date format

fig = px.bar(df, x='Date', y='Number of Invoices', title='Invoices by Date')

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

