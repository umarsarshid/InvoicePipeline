import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import requests

# MongoDB connection setup
client = MongoClient('mongodb://mongodb:27017/', username='root', password='example')
db = client.ecommerce
collection = db.invoices

# Streamlit layout
st.markdown('Explore invoice data from MongoDB.')

# Sidebar filters
customer_id = st.sidebar.selectbox('Select Customer ID', collection.distinct('customer_id'))
# Fetching top-performing products data from FastAPI
response = requests.get('http://producer:8000/top_performing_products/')
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)
print(df.head())

df['description'] = df['_id'].apply(lambda x: x['description'])
df.drop('_id', axis=1, inplace=True)

# Visualization
st.title('Top Performing Products and Categories')

# Top Categories Bar Chart
top_categories = df.groupby('description')['total_sales'].sum().reset_index().sort_values('total_sales', ascending=False)
fig_categories = px.bar(top_categories, x='description', y='total_sales', title='Top Performing Categories')
st.plotly_chart(fig_categories)

# Detailed Product Performance within Top Category
top_category = top_categories.iloc[0]['description']
top_products_in_category = df[df['description'] == top_category]
fig_products = px.bar(top_products_in_category, x='description', y='total_sales', title=f'Top Performing Products in {top_category}')
st.plotly_chart(fig_products)

# Fetch sales trends data
response2 = requests.get('http://producer:8000/sales_trends/')
data2 = response2.json()

# Convert to DataFrame
df2= pd.DataFrame(data2)
# Combine year, month, day to a single date column for plotting
df2['date'] = pd.to_datetime(df2['_id'].apply(lambda x: f"{x['year']}-{x['month']}-{x['day']}"))
df2.sort_values('date', inplace=True)

# Plot
fig2 = px.line(df, x='date', y='daily_sales', title='Daily Sales Trends')
st.plotly_chart(fig)