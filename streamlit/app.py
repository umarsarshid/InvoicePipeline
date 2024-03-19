import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# MongoDB connection setup
client = MongoClient('mongodb://mongodb:27017/', username='root', password='example')
db = client.ecommerce
collection = db.invoices

# Streamlit layout
st.markdown('Explore invoice data from MongoDB.')

# Sidebar filters
customer_id = st.sidebar.selectbox('Select Customer ID', collection.distinct('customer_id'))
# Assume 'date' field exists and is of

# Aggregate invoices by date
# pipeline = [
#     {"$group": {"_id": "$date", "count": {"$sum": 1}}},
#     {"$sort": {"_id": 1}}  # Sort by date ascending
# ]

# invoices_by_date = list(collection.aggregate(pipeline))
# Fetch data from MongoDB and load it into a DataFrame
documents = list(collection.find())
df = pd.DataFrame(documents)

# Assuming your MongoDB documents have 'invoice_date', 'price', 'quantity', 'category', 'payment_method'
# Convert 'invoice_date' to datetime format and calculate 'total_sales'
# Convert 'invoice_date' to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')


# App title
st.title("Sales Over Time Dashboard")

# Total sales over time (daily, weekly, monthly)
st.subheader("Total Sales Over Time")

# Daily Sales
df_daily = df.resample('D', on='date').totalPrice.sum()
fig_daily = px.line(df_daily, x=df_daily.index, y='totalPrice', title='Daily Sales')
st.plotly_chart(fig_daily)

# Weekly Sales
df_weekly = df.resample('W', on='date').totalPrice.sum()
fig_weekly = px.line(df_weekly, x=df_weekly.index, y='totalPrice', title='Weekly Sales')
st.plotly_chart(fig_weekly)

# Monthly Sales
df_monthly = df.resample('M', on='date').totalPrice.sum()
fig_monthly = px.line(df_monthly, x=df_monthly.index, y='totalPrice', title='Monthly Sales')
st.plotly_chart(fig_monthly)

# Sales by Category Over Time
st.subheader("Sales by Category Over Time")
df_category = df.groupby([pd.Grouper(key='date', freq='M'), 'category']).totalPrice.sum().reset_index()
fig_category = px.line(df_category, x='date', y='totalPrice', color='category', title='Monthly Sales by Category')
st.plotly_chart(fig_category)

# Sales Trends by Payment Method
st.subheader("Sales Trends by Payment Method")
df_payment = df.groupby([pd.Grouper(key='date', freq='M'), 'payment_method']).totalPrice.sum().reset_index()
fig_payment = px.line(df_payment, x='date', y='totalPrice', color='payment_method', title='Monthly Sales by Payment Method')
st.plotly_chart(fig_payment)

# Interactive Feature: Select Time Frame
st.subheader("Interactive: Explore Sales in a Specific Time Frame")
start_date = st.date_input('Start date', value=pd.to_datetime('2021-01-01'))
end_date = st.date_input('End date', value=pd.to_datetime('2021-12-31'))
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
fig_filtered = px.line(filtered_df.resample('M', on='date').totalPrice.sum(), x=filtered_df.resample('M', on='date').totalPrice.sum().index, y='totalPrice', title=f'Monthly Sales from {start_date} to {end_date}')
st.plotly_chart(fig_filtered)