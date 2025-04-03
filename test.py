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
    "1203240076": ("D 184 ABUL FAZAL ENCLAVE, JAMIA NAGAR, OKHLA, NEW DELHI 25", "Midrise Apartment (G+5)"),
    "1203240078": ("D 184 ABUL FAZAL ENCLAVE, JAMIA NAGAR, OKHLA, NEW DELHI 25", "Midrise Apartment (G+5)"),
    "1203240075": ("A 48/B, Third Floor, Abul Fazal Enclave Part II, New Delhi", "Residential"),
    "1201240077": ("448, Sector-9, Pocket-1 DDA Flats Dwarka, New Delhi-110075", "Residential"),
    "1201240072": ("448, Sector-9, Pocket-1 DDA Flats Dwarka, New Delhi-110075", "Residential"),
    "1203240079": ("C-403, Prince Apartments, Plot 54, I.P. Extension, Patparganj, Delhi - 110092", "Residential, Multi-family"),
    "1201240079": ("B-3/527, Ekta Gardens Apts, Patparganj, Delhi - 110092", "Residential"),
    "1201240085": ("B-3/527, Ekta Gardens Apts, Patparganj, Delhi - 110092", "Residential"),
    "1203240083": ("Flat No. 25, Tower E2, Sector E1, Vasant Kunj, New Delhi", "Residential"),
    "1203240073": ("Flat no. 495, Block 14, Kaveri Apartments, D6, Vasant Kunj, Delhi - 110070", "Residential"),
    "1203240074": ("569 sector A pocket C Vasant Kunj, Delhi - 110070", "Residential"),
    "1201240076": ("H No.-296 Near Durga Ashram, Chhatarpur, Delhi-110074", "Residential"),
    "1212230160": ("H No.-296 Near Durga Ashram, Chhatarpur, Delhi-110074", "Residential"),
    "1202240009": ("D-13A 2nd Floor Left side, Paryavaran Complex, Delhi 1100030", "Office"),
    "1202240008": ("D-13A 2nd Floor Left side, Paryavaran Complex, Delhi 1100030", "Office"),
    "1201240073": ("569 sector A pocket C Vasant Kunj, Delhi - 110070", "Residential"),
    "1203240080": ("F-5, 318-N, Chirag Delhi, Delhi-110017", "Residential"),
    "1201240074": ("F-5, 318-N, Chirag Delhi, Delhi-110017", "Residential"),
    "1203240077": ("B-2/51-A, Keshav Puram", "Apartment"),
    "1203240082": ("B-2/51-A, Keshav Puram", "Apartment"),
    "1202240029": ("St. Mary's School, Dwarka Sec-19", "Office"),
    "1202240028": ("St. Mary's School, Dwarka Sec-19", "Office"),
    "1202240010": ("St. Mary's School, Dwarka Sec-19", "Office"),
    "1202240012": ("St. Mary's School, Dwarka Sec-19", "School")
}

# Function to plot and display feature heatmaps in Streamlit (your existing function)
def plot_and_display_feature_heatmaps(df, features, year, month):
    # ... (the rest of the existing function)

# Streamlit app
st.title("CABH Indoor Air Quality Monitoring")

# User inputs
device_id = st.text_input("Enter Device ID:", value="1202240012")
year = st.number_input("Select Year:", min_value=2024, max_value=2025, value=2024)
month = st.selectbox("Select Month:", list(range(1, 13)))

# Display device information
if device_id.strip():
    device_details = device_info.get(device_id)
    if device_details:
        st.subheader(f"Device Information for {device_id}")
        st.write(f"**Address:** {device_details[0]}")
        st.write(f"**Typology:** {device_details[1]}")
    else:
        st.warning("No information found for this Device ID.")

# Button to generate heatmaps
if st.button("Generate Heatmaps"):
    if not device_id.strip():
        st.error("Device ID cannot be empty.")
        st.stop()
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Query to fetch data
        query = """
        SELECT id, deviceID, datetime, pm25, pm10, aqi, co2, voc, temp, humidity, battery, viral_index
        FROM reading_db
        WHERE deviceID = %s AND YEAR(datetime) = %s AND MONTH(datetime) = %s;
        """
        cursor.execute(query, (device_id, year, month))
        rows = cursor.fetchall()
        st.success("Data fetched successfully.")
        if rows:
            # Process data
            df = pd.DataFrame(rows, columns=["id", "deviceID", "datetime", "pm25", "pm10", "aqi", "co2", "voc", "temp", "humidity", "battery", "viral_index"])
            df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
            df.set_index('datetime', inplace=True)

            # Generate heatmaps and statistics
            pollutants = ['aqi', 'pm25', 'pm10', 'co2', 'voc']
            plot_and_display_feature_heatmaps(df, pollutants, year, month)

        else:
            st.warning("No data found for the given Device ID and selected month.")

    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")  # Handle unexpected errors
    finally:
        # Ensure the database connection is closed
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            st.info("Database connection closed.")
