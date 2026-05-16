import streamlit as st
import pandas as pd
import joblib
import folium

from datetime import datetime
from streamlit_folium import st_folium

current_year = datetime.now().year

df = pd.read_csv("traffic.csv")

current_time = datetime.now()

st.write(
    f"📅 Date: {current_time.strftime('%d-%m-%Y')}"
)

st.write(
    f"⏰ Time: {current_time.strftime('%I:%M:%S %p')}"
)


st.sidebar.subheader("Current Time")

st.sidebar.write(
    current_time.strftime('%d-%m-%Y %I:%M:%S %p')
)

# Convert datetime column
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Create features
df['hour'] = df['DateTime'].dt.hour
df['day'] = df['DateTime'].dt.day
df['month'] = df['DateTime'].dt.month
df['year'] = df['DateTime'].dt.year

st.sidebar.title("About Project")

st.sidebar.info(
    """
    Smart Traffic Prediction System
    using Machine Learning.

    Predicts traffic volume based on:
    - Hour
    - Day
    - Month
    - Year
    - Junction
    """
)

# Load trained model
model = joblib.load("traffic_model.pkl")

# Title
st.title("🚦 Smart Traffic Prediction System")

st.write("Predict traffic volume using Machine Learning")

# User Inputs
hour = st.slider("Hour", 0, 23, 12)

day = st.slider("Day", 1, 31, 15)

month = st.slider("Month", 1, 12, 5)

year = st.slider(
    "Year",
    2015,
    current_year + 5,
    current_year
)

junction = st.selectbox("Junction", [1, 2, 3, 4])

# Prediction Button
if st.button("Predict Traffic"):

    sample = pd.DataFrame({
        'hour': [hour],
        'day': [day],
        'month': [month],
        'year': [year],
        'Junction': [junction]
    })

    prediction = model.predict(sample)

    traffic = prediction[0]

    # Prediction Result
    st.success(
        f"Predicted Traffic Volume: {traffic:.2f}"
    )

    # Metric
    st.metric(
        label="Predicted Vehicles",
        value=f"{traffic:.0f}"
    )

    # Traffic Status
    if traffic < 50:
        st.success("🟢 Low Traffic")

    elif traffic < 100:
        st.warning("🟡 Moderate Traffic")

    else:
        st.error("🔴 Heavy Traffic")

st.subheader("Traffic Trend by Hour")

traffic_by_hour = df.groupby('hour')['Vehicles'].mean()

st.line_chart(traffic_by_hour)

# Heavy Traffic Zone

# User Location Input
city = st.text_input(
    "📍 Enter City",
    "Delhi"
)

# City Coordinates
city_coords = {

    "Delhi": [28.6139, 77.2090],

    "Mumbai": [19.0760, 72.8777],

    "Bangalore": [12.9716, 77.5946],

    "Chennai": [13.0827, 80.2707],

    "Kolkata": [22.5726, 88.3639],

    "Hyderabad": [17.3850, 78.4867],

    "Gurgaon": [28.4595, 77.0266]
}

# Get Coordinates
coords = city_coords.get(
    city,
    [28.6139, 77.2090]
)

# Map
st.subheader("🌍 Traffic Congestion Map")

m = folium.Map(
    location=coords,
    zoom_start=11
)

# Marker
folium.CircleMarker(

    location=coords,

    radius=20,

    popup=f"Traffic in {city}",

    color='red',

    fill=True,

    fill_color='red'

).add_to(m)

# Show Map
st_folium(m, width=700)
