import streamlit as st
import pandas as pd
import numpy as np
import pymongo
import random
from faker import Faker
from pymongo import MongoClient

fake = Faker()

def generate_random_data(num_records):
    stations = ['Caracol TV', 'SRCN', 'RCN']
    formats = ['Creative A', 'Creative B', 'Creative C']
    days = ['MTuWTHF', 'MTuWThF', 'MTuWThFSa']
    times = ['9 AM-3PM', '10 AM-2PM']
    
    data = {
        'Station': [random.choice(stations) for _ in range(num_records)],
        'Week': [fake.date_this_year().strftime("%m/%d/%Y") for _ in range(num_records)],
        'Format': [random.choice(formats) for _ in range(num_records)],
        'Creative': [f"Creative {random.choice(['A', 'B', 'C'])}" for _ in range(num_records)],
        'Length': [f"{random.choice([30, 60])} seconds" for _ in range(num_records)],
        'Days': [random.choice(days) for _ in range(num_records)],
        'Times': [random.choice(times) for _ in range(num_records)],
        'Rate': [random.randint(50, 150) for _ in range(num_records)],
        'Quantity': [random.randint(5, 20) for _ in range(num_records)],
    }
    
    # Calculate Cost, Revenue, Profit, and other financial metrics based on the generated data
    data['Cost'] = [round(data['Rate'][i] * data['Quantity'][i] * random.uniform(0.8, 1.2), 2) for i in range(num_records)]
    data['Revenue'] = [round(data['Cost'][i] * random.uniform(1.5, 2.5), 2) for i in range(num_records)]
    data['Profit'] = [round(data['Revenue'][i] - data['Cost'][i], 2) for i in range(num_records)]
    data['Margin'] = [f"{round((data['Profit'][i] / data['Revenue'][i]) * 100, 2)}%" for i in range(num_records)]
    data['Revenue Per Cost'] = [round(data['Revenue'][i] / data['Cost'][i], 2) for i in range(num_records)]
    data['Per Call'] = [round(random.uniform(10, 50), 2) for _ in range(num_records)]
    data['Unique Calls'] = [random.randint(5, 20) for _ in range(num_records)]
    
    # Convert numeric columns to formatted strings
    data['Rate'] = [f"${rate}.00" for rate in data['Rate']]
    data['Cost'] = [f"${cost}" for cost in data['Cost']]
    data['Revenue'] = [f"${revenue}" for revenue in data['Revenue']]
    data['Profit'] = [f"${profit}" for profit in data['Profit']]
    data['Revenue Per Cost'] = [f"${rpc}" for rpc in data['Revenue Per Cost']]
    data['Per Call'] = [f"${pc}" for pc in data['Per Call']]

    return pd.DataFrame(data)

def submit_to_mongodb(df):
    # Connect to MongoDB
    client = MongoClient(f'mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/')
    # client = MongoClient(f'mongodb+srv://mdebinski:<Passcode here>@mytestcluster.5bfpq.mongodb.net/')
    client.admin.command('ping')
    print("Connection to MongoDB established successfully.")
    db = client['ReportSimulatorDatabase']
    collection = db['UnrandomizedRepSimCollection']

    # Convert DataFrame to dictionary
    data_dict = df.to_dict(orient='records')

    # Insert data into MongoDB
    collection.insert_many(data_dict)

st.title('Random Data Generator')

num_records = st.number_input('Number of Records', min_value=1, value=10)

if st.button('Generate Data'):
    df = generate_random_data(num_records)
    st.write(df)

    # Store the generated DataFrame in session state
    st.session_state.df = df

if st.button('Submit to MongoDB'):
    if 'df' in st.session_state:
        submit_to_mongodb(st.session_state.df)
        st.success('Data submitted to MongoDB successfully!')
    else:
        st.error('No data available to submit. Please generate data first.')
