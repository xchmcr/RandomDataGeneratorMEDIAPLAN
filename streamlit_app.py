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
        'Rate': [f"${random.randint(50, 150)}.00" for _ in range(num_records)],
        'Quantity': [random.randint(5, 20) for _ in range(num_records)],
        'Cost': [f"${random.randint(500, 2000)}.00" for _ in range(num_records)],
        'Revenue': [f"${random.randint(1000, 5000)}.00" for _ in range(num_records)],
        'Profit': [f"${random.randint(500, 3000)}.00" for _ in range(num_records)],
        'Margin': [f"{random.randint(50, 70)}%" for _ in range(num_records)],
        'Revenue Per Cost': [f"${random.randint(50, 300)}.00" for _ in range(num_records)],
        'Per Call': [f"${random.randint(10, 50)}.00" for _ in range(num_records)],
        'Unique Calls': [random.randint(5, 20) for _ in range(num_records)],
    }
    
    return pd.DataFrame(data)

def submit_to_mongodb(df):
    # Connect to MongoDB
    client = MongoClient(f'mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/')
    # client = MongoClient(f'mongodb+srv://mdebinski:<Passcode here>@mytestcluster.5bfpq.mongodb.net/')
    client.admin.command('ping')
    print("Connection to MongoDB established successfully.")
    db = client['ReportSimulatorDatabase']
    collection = db['ReportSimulatorCollection']

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
