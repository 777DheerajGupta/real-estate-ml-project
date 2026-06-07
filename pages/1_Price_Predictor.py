import streamlit as st
import pandas as pd
import numpy as np
from model_loader import load_pickle

# Load only what this page needs
@st.cache_resource
def load_models():
    with st.spinner("Loading prediction model..."):
        pipeline = load_pickle("pipeline.pkl")
        df       = load_pickle("df.pkl")
    return pipeline, df

pipeline, df = load_models()

st.title("Real Estate Price Prediction")

# User Input Section
st.header('Enter Your Inputs')

# Property Type (Categorical)
property_type = st.selectbox('Property Type', df['property_type'].unique().tolist(), key="property_type")

# Sector (Categorical)
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()), key="sector")

# Number of Bedrooms (Numeric)
bedrooms = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].dropna().unique().tolist()), key="bedrooms")
bedrooms = float(bedrooms)  # Convert to float

# Number of Bathrooms (Numeric)
bathroom = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].dropna().unique().tolist()), key="bathroom")
bathroom = float(bathroom)  # Convert to float

# Balconies (Categorical)
balcony = st.selectbox('Balconies', sorted(df['balcony'].dropna().unique().tolist()), key="balcony")

# Property Age (Categorical)
property_age = st.selectbox('Property Age', sorted(df['agePossession'].dropna().unique().tolist()), key="property_age")

# Built-Up Area (Numeric)
built_up_area = float(st.number_input("Built-Up Area (in sqft)", key="built_up_area"))

# Servant Room (Numeric)
servant_room = st.selectbox("Servant Room", sorted(df['servant room'].dropna().unique().tolist()), key="servant_room")
servant_room = float(servant_room)  # Convert to float

# Store Room (Numeric)
store_room = st.selectbox("Store Room", sorted(df['store room'].dropna().unique().tolist()), key="store_room")
store_room = float(store_room)  # Convert to float

# Furnishing Type (Categorical)
furnishing_type = st.selectbox("Furnishing Type", df['furnishing_type'].unique().tolist(), key="furnishing_type")

# Luxury Category (Categorical)
luxury_category = st.selectbox("Luxury Category", df['luxury_category'].unique().tolist(), key="luxury_category")

# Floor Category (Categorical)
floor_category = st.selectbox("Floor Category", df['floor_category'].unique().tolist(), key="floor_category")

# Submit Button
if st.button("predict"):
    data = [[
        property_type,  # house
        sector,  # sector 102
        bedrooms,  # 4.0
        bathroom,  # 3.0
        balcony,  # 3+
        property_age,  # New Property
        built_up_area,  # 2750.0
        servant_room,  # 0.0
        store_room,  # 0.0
        furnishing_type,  # unfurnished
        luxury_category,  # Low
        floor_category  # Low Floor
    ]]

    # Column names swapped with actual values
    columns = [
        'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category'
    ]

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # Display DataFrame
    # st.dataframe(one_df)

    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.18
    high = base_price + 0.18

    st.text("The Price Of the flat is between {} Cr and {} Cr".format(    round(low,2) , round(high,2)))