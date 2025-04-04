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

# Streamlit app
st.title("CABH Indoor Air Quality Monitoring")

# Define pollutant display names
pollutant_display_names = {
    'aqi': 'AQI',
    'pm25': 'PM 2.5',
    'pm10': 'PM 10',
    'co2': 'CO₂',
    'voc': 'VOC'
}

# Function to plot and display heatmaps
def plot_and_display_feature_heatmaps(df, features, year, month):
    feature_boundaries = {
        'aqi': [0, 50, 100, 150, 200, 300, 500],
        'pm25': [0, 12, 35, 55, 150, 250, 500],
        'pm10': [0, 20, 50, 100, 250, 350, 500],
        'co2': [0, 900, 10000],
        'voc': [0, 500, 1000]
    }
    
    color_list = ['#006400', '#228B22', '#FFFF00', '#FF7F00', '#FF0000', '#8B0000']
    cmap = ListedColormap(color_list)
    
    for feature in features:
        feature_data = df[(df.index.year == year) & (df.index.month == month)][feature]
        
        if feature_data.empty:
            st.warning(f"No data available for {pollutant_display_names.get(feature, feature)} in {calendar.month_name[month]} {year}.")
            continue

        fig, ax = plt.subplots(figsize=(10, 6))
        norm = BoundaryNorm(feature_boundaries[feature], cmap.N)
        
        # Prepare the calendar heatmap
        num_days = calendar.monthrange(year, month)[1]
        calendar_data = np.full((5, 7), np.nan)
        first_day = calendar.monthrange(year, month)[0]
        
        for day in range(1, num_days + 1):
            day_values = feature_data[feature_data.index.day == day]
            if not day_values.empty:
                daily_avg = day_values.mean()
                week_row, week_col = divmod(day + first_day - 1, 7)
                if week_row < 5:
                    calendar_data[week_row, week_col] = daily_avg

        sns.heatmap(calendar_data, annot=True, fmt=".0f", cmap=cmap, norm=norm,
                    cbar=False, xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    yticklabels=[1, 2, 3, 4, 5], ax=ax, linewidths=1, linecolor='black')
        
        ax.set_title(f"{calendar.month_name[month]} {year} - {pollutant_display_names.get(feature, feature)}", fontsize=14)
        ax.set_xlabel("Day of the Week", fontsize=12)
        ax.set_ylabel("Week", fontsize=12)
        
        st.pyplot(fig)
        plt.close()

# Streamlit UI
device_id = st.text_input("Enter Device ID:", value="1202240012")
year = st.number_input("Select Year:", min_value=2024, max_value=2025, value=2024)
month = st.selectbox("Select Month:", list(range(1, 13)))

if st.button("Generate Heatmaps"):
    if not device_id.strip():
        st.error("Device ID cannot be empty.")
    else:
        try:
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
            cursor = conn.cursor()
            query = """
            SELECT datetime, pm25, pm10, aqi, co2, voc
            FROM reading_db
            WHERE deviceID = %s AND YEAR(datetime) = %s AND MONTH(datetime) = %s;
            """
            cursor.execute(query, (device_id, year, month))
            rows = cursor.fetchall()
            
            if rows:
                df = pd.DataFrame(rows, columns=["datetime", "pm25", "pm10", "aqi", "co2", "voc"])
                df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
                df.set_index('datetime', inplace=True)
                plot_and_display_feature_heatmaps(df, pollutant_display_names.keys(), year, month)
            else:
                st.warning("No data found for the given Device ID and selected month.")
        except mysql.connector.Error as e:
            st.error(f"Database error: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                st.info("Database connection closed.")
