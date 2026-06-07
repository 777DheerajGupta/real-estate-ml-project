import streamlit as st

st.set_page_config(
    page_title="Real Estate Insights",
    page_icon="🏠",
    layout="wide"
)

# Title and Header
st.title("Welcome to Real Estate Insights!")
st.subheader("Get Price Predictions, Trend Analysis, and Apartment Recommendations")

st.write("Explore our powerful features to assist with your real estate needs:")

# Feature 1: Price Predictor
st.subheader("🏠 Price Predictor")
st.write("Find out the estimated price of your property using our advanced prediction tool.")
if st.button("Go to Price Predictor →"):
    st.switch_page("pages/1_Price_Predictor.py")

# Feature 2: Data Analysis
st.subheader("📊 Data Analysis")
st.write("Analyze property data and uncover real estate trends.")
if st.button("Analyze Your Data →"):
    st.switch_page("pages/2_AnalysisApp.py")

# Feature 3: Recommend Apartment
st.subheader("🔍 Recommend Apartment")
st.write("Find your dream apartment with recommendations tailored to your preferences.")
if st.button("Find Apartments →"):
    st.switch_page("pages/3_RecommendAppartments.py")

st.write("---")
st.write("Need help or have feedback? Contact us!")