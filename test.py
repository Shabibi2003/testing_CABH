import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import calendar
from matplotlib.colors import ListedColormap, BoundaryNorm

# Database connection details
host = "139.59.34.149"
user = "neemdb"
password = "(#&pxJ&p7JvhA7<B"
database = "cabh_iaq_db"

# Device information dictionary (mapping device ID to address and typology)
device_info = {
    "1201240075": ("Hines Office, 12th Floor, One Horizon Centre, Sec-43, Gurugram", "Office"),
    "1201240078": ("Hines Office, 12th Floor, One Horizon Centre, Sec-43, Gurugram", "Office"),
    "1202240026": ("D-1/25 Vasant Vihar, New Delhi-110057(EDS Delhi)", "Office"),
    "1202240025": ("D-1/25 Vasant Vihar, New Delhi-110057(EDS Delhi)", "Office"),
    "1203240081": ("26A Poorvi Marg, Vasant Vihar, New Delhi-110057 (EDS, E-Block, Delhi)", "Office"),
    "1202240011": ("D-188, Abul Fazal Enclave-I, Jamia Nagar, New Delhi-110025", "Apartment"),
    "1202240027": ("D-188, Abul Fazal Enclave-I, Jamia Nagar, New Delhi-110025", "Apartment"),
    # Add all other devices...
}

# Function to fetch data from MySQL based on device_id, year, and month
def fetch_data_from_db(device_id, year, month):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Query to fetch data for the device
        query = """
        SELECT id, deviceID, datetime, pm25, pm10, aqi, co2, voc, temp, humidity, battery, viral_index
        FROM reading_db
        WHERE deviceID = %s AND YEAR(datetime) = %s AND MONTH(datetime) = %s;
        """

        # Fetch the data
        df = pd.read_sql(query, connection)
        df['datetime'] = pd.to_datetime(df['datetime'])
        connection.close()
        return df

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Function to plot and display feature heatmaps in Streamlit
def plot_and_display_feature_heatmaps(df, features, year, month):
    if df.empty:
        st.warning("No data available for the selected device and time period.")
        return

    feature_boundaries = {
        'aqi': [0, 50, 100, 150, 200, 300, 500],
        'pm25': [0, 12, 35, 55, 150, 250, 500],
        'pm10': [0, 20, 50, 100, 250, 350, 500],
        'co2': [0, 900, 10000],
        'voc': [0, 500, 1000]
    }

    feature_labels = {
        'aqi': ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe'],
        'pm25': ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe'],
        'pm10': ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe'],
        'co2': ['Good', 'Poor'],
        'voc': ['Good', 'Poor']
    }

    # Filter data for the selected month and year
    for feature in features:
        feature_data = df[(df.index.year == year) & (df.index.month == month)][feature]

        if feature_data.empty:
            st.warning(f"No data available for {feature} in {calendar.month_name[month]} {year}.")
            continue

        # Plotting the heatmap
        fig, ax = plt.subplots(figsize=(10, 6))

        color_list = ['#006400', '#228B22', '#FFFF00', '#FF7F00', '#FF0000', '#8B0000']
        cmap = ListedColormap(color_list)

        boundaries = feature_boundaries[feature]
        labels = feature_labels[feature]

        if len(boundaries) - 1 != len(labels):
            labels = labels[:-1]

        # Prepare the calendar data (5 weeks in a month)
        num_days = calendar.monthrange(year, month)[1]
        calendar_data = np.full((5, 7), np.nan)

        for day in range(1, num_days + 1):
            day_values = feature_data[feature_data.index.day == day]
            if not day_values.empty:
                daily_avg = day_values.mean()
                first_day_of_month = calendar.monthrange(year, month)[0]
                week_row = (day + first_day_of_month - 1) // 7
                week_col = (day + first_day_of_month - 1) % 7

                if week_row < 5:
                    calendar_data[week_row, week_col] = daily_avg

        norm = BoundaryNorm(boundaries, cmap.N)
        sns.heatmap(calendar_data, annot=True, fmt=".0f", cmap=cmap, norm=norm,
                    cbar=False, xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    yticklabels=[1, 2, 3, 4, 5], ax=ax, linewidths=1, linecolor='black')

        ax.set_title(f"{calendar.month_name[month]} {year} - {feature}", fontsize=14)
        ax.set_xlabel("Day of the Week", fontsize=12)
        ax.set_ylabel("Week of the Month", fontsize=12)

        st.pyplot(fig)

# Streamlit UI
st.title("Air Quality Dashboard")

# Select device ID
device_id = st.selectbox("Select Device ID", list(device_info.keys()))
st.write(f"Device Information: {device_info.get(device_id)}")

# Select year and month
year = st.slider("Select Year", min_value=2020, max_value=2025, value=2023)
month = st.slider("Select Month", min_value=1, max_value=12, value=1)

# Fetch data
df = fetch_data_from_db(device_id, year, month)

# List of features to plot
features = ['aqi', 'pm25', 'pm10', 'co2', 'voc']

# Display the heatmaps
plot_and_display_feature_heatmaps(df, features, year, month)
