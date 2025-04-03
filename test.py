import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import calendar
from matplotlib.colors import ListedColormap, BoundaryNorm
import json

# Database connection details
host = "139.59.34.149"
user = "neemdb"
password = "(#&pxJ&p7JvhA7<B"
database = "cabh_iaq_db"

# Example raw text (use the actual text you have here)
device_info_text = """
{
    "ApiResponse": "Success",
    "RowCount": 31,
    "Data": [
       {
    "ApiResponse": "Success",
    "RowCount": 31,
    "Data": [
        {
            "deviceID": "1201240075",
            "deployementID": "OFGSI-005",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-02-21 00:00:00",
            "uninstallation_date": null,
            "address": "Hines Office, 12th Floor, One Horizon Centre, Sec-43, Gurugram",
            "latitude": "28.456",
            "longitude": "77.0956",
            "nearby_AQI_station": "Sector-51, Gurugram-HSPCB (3.5 kms)",
            "outdoor_deviceID": "CPCB1703205345",
            "contact_person": "Mr. Dharmendra Singh (Assistant Manager-IT)",
            "contact_number": "9716820034",
            "emailID": "Ashwin.Bhakay@hines.com , Dharmendra.Singh@hines.c",
            "total_no_of_floors": "25",
            "installation_floor_no": "12",
            "total_build_up_area_sq_m": "0",
            "occupancy": "25",
            "created_on": "2024-08-20 04:41:16",
            "updated_on": "2024-08-20 04:41:16"
        },
        {
            "deviceID": "1201240078",
            "deployementID": "OFGSI-006",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-02-21 00:00:00",
            "uninstallation_date": null,
            "address": "Hines Office, 12th Floor, One Horizon Centre, Sec-43, Gurugram",
            "latitude": "28.45",
            "longitude": "77.095",
            "nearby_AQI_station": "Sector-51, Gurugram-HSPCB (3.5 kms)",
            "outdoor_deviceID": "CPCB1703205345",
            "contact_person": "Mr. Dharmendra Singh (Assistant Manager-IT)",
            "contact_number": "9716820034",
            "emailID": "Ashwin.Bhakay@hines.com , Dharmendra.Singh@hines.c",
            "total_no_of_floors": "25",
            "installation_floor_no": "12",
            "total_build_up_area_sq_m": "0",
            "occupancy": "15",
            "created_on": "2024-05-13 10:38:26",
            "updated_on": "2024-05-13 10:38:26"
        },
        {
            "deviceID": "1202240026",
            "deployementID": "OFRK-11",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-18 00:00:00",
            "uninstallation_date": null,
            "address": "D-1/25 Vasant Vihar , New Delhi-110057(EDS Delhi)",
            "latitude": "28.5625",
            "longitude": "77.1497",
            "nearby_AQI_station": "RK Puram Delhi-DPCC (2.5 Kms)",
            "outdoor_deviceID": "THIRD_DPCC_SCR_RKPURAM",
            "contact_person": "Mr. Abhishek Soni",
            "contact_number": "9310646239",
            "emailID": "Soni.abhishek@edsglobal.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "-1",
            "total_build_up_area_sq_m": "464",
            "occupancy": "28",
            "created_on": "2024-09-12 04:54:12",
            "updated_on": "2024-09-12 04:54:12"
        },
        {
            "deviceID": "1202240025",
            "deployementID": "OFRK-12",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-18 00:00:00",
            "uninstallation_date": null,
            "address": "D-1/25 Vasant Vihar , New Delhi-110057(EDS Delhi)",
            "latitude": "28.562",
            "longitude": "77.149",
            "nearby_AQI_station": "RK Puram Delhi-DPCC (2.5 Kms)",
            "outdoor_deviceID": "THIRD_DPCC_SCR_RKPURAM",
            "contact_person": "Mr. Abhishek Soni",
            "contact_number": "9310646239",
            "emailID": "Soni.abhishek@edsglobal.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "-1",
            "total_build_up_area_sq_m": "464",
            "occupancy": "28",
            "created_on": "2024-05-13 10:35:00",
            "updated_on": "2024-05-13 10:35:00"
        },
        {
            "deviceID": "1203240081",
            "deployementID": "OFRK-26",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-09-20 00:00:00",
            "uninstallation_date": null,
            "address": "26A Poorvi Marg, Vasant Vihar , New Delhi-110057\r\n(EDS, E-Block, Delhi)",
            "latitude": "28.5614",
            "longitude": "77.1584",
            "nearby_AQI_station": "RK Puram Delhi-DPCC (2 Kms)",
            "outdoor_deviceID": "THIRD_DPCC_SCR_RKPURAM",
            "contact_person": "Abhishek Soni",
            "contact_number": "9310646239",
            "emailID": "Soni.abhishek@edsglobal.com",
            "total_no_of_floors": "3",
            "installation_floor_no": "0",
            "total_build_up_area_sq_m": "0",
            "occupancy": "12",
            "created_on": "2024-09-30 08:51:25",
            "updated_on": "2024-09-30 08:51:25"
        },
        {
            "deviceID": "1202240011",
            "deployementID": "RECR-15",
            "typology": "Apartment",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-04-05 00:14:07",
            "uninstallation_date": null,
            "address": "D-188, Abul Fazal Enclave-I, Jamia Nagar, New Delhi-110025",
            "latitude": "28.5557",
            "longitude": "77.2948",
            "nearby_AQI_station": "CRRI Mathura Road, Delhi-IMD(2Km)",
            "outdoor_deviceID": "DELCPCB010",
            "contact_person": "Mariyam",
            "contact_number": "9718224396",
            "emailID": "mariyam.zakiah2020@gmail.com",
            "total_no_of_floors": "3",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "40",
            "occupancy": "3",
            "created_on": "2024-09-12 05:35:20",
            "updated_on": "2024-09-12 05:35:20"
        },
        {
            "deviceID": "1202240027",
            "deployementID": "RECR-16",
            "typology": "Apartment",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-04-05 14:07:00",
            "uninstallation_date": null,
            "address": "D-188, Abul Fazal Enclave-I, Jamia Nagar, New Delhi-110025",
            "latitude": "28.5555",
            "longitude": "77.2942",
            "nearby_AQI_station": "CRRI Mathura Road, Delhi-IMD(2Km)",
            "outdoor_deviceID": "DELCPCB010",
            "contact_person": "Mariyam",
            "contact_number": "9718224396",
            "emailID": "mariyam.zakiah2020@gmail.com",
            "total_no_of_floors": "3",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "60",
            "occupancy": "3",
            "created_on": "2024-06-24 10:18:42",
            "updated_on": "2024-06-24 10:18:42"
        },
        {
            "deviceID": "1203240076",
            "deployementID": "RECR-23",
            "typology": "Midrise Apartment (G+5)",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-05-05 00:00:00",
            "uninstallation_date": null,
            "address": "D 184 ABUL FAZAL ENCLAVE, JAMIA NAGAR, OKHLA, NEW DELHI 25",
            "latitude": "28.559",
            "longitude": "77.293",
            "nearby_AQI_station": "CRRI Mathura Road, Delhi-IMD (2Km)",
            "outdoor_deviceID": "DELCPCB010",
            "contact_person": "Hisham Ahmed",
            "contact_number": "9873065488",
            "emailID": "hisham@edsglobal.com",
            "total_no_of_floors": "5",
            "installation_floor_no": "5",
            "total_build_up_area_sq_m": "135",
            "occupancy": "4",
            "created_on": "2024-08-20 06:09:34",
            "updated_on": "2024-08-20 06:09:34"
        },
        {
            "deviceID": "1203240078",
            "deployementID": "RECR-24",
            "typology": "Midrise Apartment (G+5)",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-05-05 00:00:00",
            "uninstallation_date": null,
            "address": "D 184 ABUL FAZAL ENCLAVE, JAMIA NAGAR, OKHLA, NEW DELHI 25",
            "latitude": "28.55",
            "longitude": "77.29",
            "nearby_AQI_station": "CRRI Mathura Road, Delhi-IMD (2Km)",
            "outdoor_deviceID": "DELCPCB010",
            "contact_person": "Hisham Ahmed",
            "contact_number": "9873065488",
            "emailID": "hisham@edsglobal.com",
            "total_no_of_floors": "5",
            "installation_floor_no": "5",
            "total_build_up_area_sq_m": "135",
            "occupancy": "4",
            "created_on": "2024-08-20 06:09:24",
            "updated_on": "2024-08-20 06:09:24"
        },
        {
            "deviceID": "1203240075",
            "deployementID": "RECR-31",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "kitchen",
            "installation_date": "2024-09-10 00:00:00",
            "uninstallation_date": null,
            "address": "A 48/B, Third Floor, Abul Fazal Enclave Part II, New Delhi",
            "latitude": "28.5503",
            "longitude": "77.2997",
            "nearby_AQI_station": "CRRI Mathura Road, Delhi-IMD (2Km)",
            "outdoor_deviceID": "DELCPCB010",
            "contact_person": "Shahzeb",
            "contact_number": "8287035226",
            "emailID": "shahzeb@edsglobal.com",
            "total_no_of_floors": "5",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "112",
            "occupancy": "3",
            "created_on": "2024-09-30 09:14:11",
            "updated_on": "2024-09-30 09:14:11"
        },
        {
            "deviceID": "1201240077",
            "deployementID": "RED8-003",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "kitchen",
            "installation_date": "2024-02-29 00:00:00",
            "uninstallation_date": null,
            "address": "448, Sector-9, Pocket-1 DDA Flats Dwarka , New Delhi-110075",
            "latitude": "28.583",
            "longitude": "77.063",
            "nearby_AQI_station": "Dwarka sector-8, Delhi-DPCC (2 Kms)",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Lakshmi Ganesh Kamath",
            "contact_number": "9811022520",
            "emailID": "Lakshmi.g.kamath@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "90",
            "occupancy": "3",
            "created_on": "2024-07-18 11:04:18",
            "updated_on": "2024-07-18 11:04:18"
        },
        {
            "deviceID": "1201240072",
            "deployementID": "RED8-004",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-02-29 00:00:00",
            "uninstallation_date": null,
            "address": "448, Sector-9, Pocket-1 DDA Flats Dwarka , New Delhi-110075",
            "latitude": "28.5835",
            "longitude": "77.0635",
            "nearby_AQI_station": "Dwarka sector-8, Delhi-DPCC (2 Kms)",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Lakshmi Ganesh Kamath",
            "contact_number": "9811022520",
            "emailID": "Lakshmi.g.kamath@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "90",
            "occupancy": "3",
            "created_on": "2024-08-20 05:37:35",
            "updated_on": "2024-08-20 05:37:35"
        },
        {
            "deviceID": "1203240079",
            "deployementID": "REPG - 29",
            "typology": "Residential, Multi-family",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living room",
            "installation_date": "2024-07-06 00:00:00",
            "uninstallation_date": null,
            "address": "C-403, Prince Apartments, Plot 54, I.P. Extension, Patparganj, Delhi - 110092",
            "latitude": "28.63",
            "longitude": "77.2983",
            "nearby_AQI_station": "Patparganj Delhi-DPCC (1.5 Kms)",
            "outdoor_deviceID": "DELDPCC006",
            "contact_person": "Piyush Varma",
            "contact_number": "9718906332",
            "emailID": "varpiyush@gmail.com",
            "total_no_of_floors": "7",
            "installation_floor_no": "4",
            "total_build_up_area_sq_m": "120",
            "occupancy": "1",
            "created_on": "2024-09-18 05:49:52",
            "updated_on": "2024-09-18 05:49:52"
        },
        {
            "deviceID": "1201240079",
            "deployementID": "REPG-001",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-02-19 00:00:00",
            "uninstallation_date": null,
            "address": "B-3/527, Ekta Gardens Apts, Patparganj, Delhi - 110092",
            "latitude": "28.6248",
            "longitude": "77.2914",
            "nearby_AQI_station": "Patparganj Delhi-DPCC (0.12 Kms)",
            "outdoor_deviceID": "DELDPCC006",
            "contact_person": "Mr. Piyush Verma",
            "contact_number": "9718906332",
            "emailID": "Piyush@edsglobal.com",
            "total_no_of_floors": "7",
            "installation_floor_no": "5",
            "total_build_up_area_sq_m": "90",
            "occupancy": "3",
            "created_on": "2024-09-12 05:44:18",
            "updated_on": "2024-09-12 05:44:18"
        },
        {
            "deviceID": "1201240085",
            "deployementID": "REPG-002",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-02-19 00:00:00",
            "uninstallation_date": null,
            "address": "B-3/527, Ekta Gardens Apts, Patparganj, Delhi - 110092",
            "latitude": "28.62",
            "longitude": "77.291",
            "nearby_AQI_station": "Patparganj Delhi-DPCC (0.12 Kms)",
            "outdoor_deviceID": "DELDPCC006",
            "contact_person": "Mr. Piyush Verma",
            "contact_number": "9718906332",
            "emailID": "Piyush@edsglobal.com",
            "total_no_of_floors": "7",
            "installation_floor_no": "5",
            "total_build_up_area_sq_m": "90",
            "occupancy": "5",
            "created_on": "2024-07-18 11:04:21",
            "updated_on": "2024-07-18 11:04:21"
        },
        {
            "deviceID": "1203240083",
            "deployementID": "RERK-032",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living room",
            "installation_date": "2024-09-14 00:00:00",
            "uninstallation_date": null,
            "address": "Flat No. 25, Tower E2, Sector E1, Vasant Kunj, New Delhi",
            "latitude": "28.5369",
            "longitude": "77.1316",
            "nearby_AQI_station": "RK Puram Delhi-DPCC (5.5 Kms)",
            "outdoor_deviceID": "THIRD_DPCC_SCR_RKPURAM",
            "contact_person": "Sheetal Jain",
            "contact_number": "9958692759",
            "emailID": "sheetal@edsglobal.com",
            "total_no_of_floors": "7",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "60",
            "occupancy": "2",
            "created_on": "2024-09-30 10:02:02",
            "updated_on": "2024-09-30 10:02:02"
        },
        {
            "deviceID": "1203240073",
            "deployementID": "RERK-27",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-07-16 00:00:00",
            "uninstallation_date": null,
            "address": "Flat no. 495, Block 14, Kaveri Apartments, D6, Vasant Kunj, Delhi - 110070",
            "latitude": "28.526",
            "longitude": "77.1518",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi - DPCC",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Nidhi",
            "contact_number": "9819898045",
            "emailID": "nidhi@edsglobal.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "3",
            "total_build_up_area_sq_m": "0",
            "occupancy": "1",
            "created_on": "2024-09-30 08:56:46",
            "updated_on": "2024-09-30 08:56:46"
        },
        {
            "deviceID": "1203240074",
            "deployementID": "RERO-28",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living room",
            "installation_date": "2024-09-15 00:00:00",
            "uninstallation_date": null,
            "address": "569 sector A pocket C Vasant Kunj, Delhi - 110070",
            "latitude": "28.7143",
            "longitude": "77.1081",
            "nearby_AQI_station": "Rohini - DPCC (2.5 Kms)",
            "outdoor_deviceID": "DELDPCC011",
            "contact_person": "Ashish Jain",
            "contact_number": "9891683061",
            "emailID": "varpiyush@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "1",
            "total_build_up_area_sq_m": "100",
            "occupancy": "6",
            "created_on": "2024-09-30 09:24:12",
            "updated_on": "2024-09-30 09:24:12"
        },
        {
            "deviceID": "1201240076",
            "deployementID": "RESA-009",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-03-06 00:00:00",
            "uninstallation_date": null,
            "address": "H No.-296 Near Durga Ashram, Chhatarpur, Delhi-110074",
            "latitude": "28.4965",
            "longitude": "77.1815",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi-DPCC (4 Kms)",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Mr. Surender Bhati",
            "contact_number": "9555864378",
            "emailID": "Surrenderbhati30@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "680",
            "occupancy": "16",
            "created_on": "2024-09-12 05:46:30",
            "updated_on": "2024-09-12 05:46:30"
        },
        {
            "deviceID": "1212230160",
            "deployementID": "RESA-010",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-03-06 00:00:00",
            "uninstallation_date": null,
            "address": "H No.-296 Near Durga Ashram, Chhatarpur, Delhi-110074",
            "latitude": "28.496",
            "longitude": "77.181",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi-DPCC (4 Kms)",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Mr. Surender Bhati",
            "contact_number": "9555864378",
            "emailID": "Surrenderbhati30@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "680",
            "occupancy": "16",
            "created_on": "2024-06-24 11:35:53",
            "updated_on": "2024-06-24 11:35:53"
        },
        {
            "deviceID": "1202240009",
            "deployementID": "RESA-13",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-03-19 00:00:00",
            "uninstallation_date": null,
            "address": "D-13A 2nd Floor Left side, Paryavaran Complex, Delhi 1100030",
            "latitude": "28.5145",
            "longitude": "77.1965",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi DPCC (2.2 Kms)",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Mr. Robin Jain",
            "contact_number": "7062137067",
            "emailID": "Robin@edsglobal.com, Robinmits.jain@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "75",
            "occupancy": "3",
            "created_on": "2024-09-12 05:48:43",
            "updated_on": "2024-09-12 05:48:43"
        },
        {
            "deviceID": "1202240008",
            "deployementID": "RESA-14",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-19 00:00:00",
            "uninstallation_date": null,
            "address": "D-13A 2nd Floor Left side, Paryavaran Complex, Delhi 1100030",
            "latitude": "28.514",
            "longitude": "77.196",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi DPCC (2.2 Kms)",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Mr. Robin Jain",
            "contact_number": "7062137067",
            "emailID": "Robin@edsglobal.com, Robinmits.jain@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "75",
            "occupancy": "3",
            "created_on": "2024-08-20 04:44:46",
            "updated_on": "2024-08-20 04:44:46"
        },
        {
            "deviceID": "1201240073",
            "deployementID": "RESA-30",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-09-15 00:00:00",
            "uninstallation_date": null,
            "address": "569 sector A pocket C Vasant Kunj, Delhi - 110070",
            "latitude": "28.5116",
            "longitude": "77.1678",
            "nearby_AQI_station": "Sri Aurobindo Marg, Delhi - DPCC (3 Kms)",
            "outdoor_deviceID": "DELDPCC018",
            "contact_person": "Tanmay Tathagat",
            "contact_number": "9711442008",
            "emailID": "tanmay@edsglobal.com",
            "total_no_of_floors": "5",
            "installation_floor_no": "1",
            "total_build_up_area_sq_m": "0",
            "occupancy": "0",
            "created_on": "2024-09-30 09:08:19",
            "updated_on": "2024-09-30 09:08:19"
        },
        {
            "deviceID": "1203240080",
            "deployementID": "RESF-007",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-06-09 00:00:00",
            "uninstallation_date": null,
            "address": "F-5, 318-N, Chirag Delhi, Delhi-110017",
            "latitude": "28.5367",
            "longitude": "77.2277",
            "nearby_AQI_station": "SiriFort, Delhi-CPCB (2 Kms)",
            "outdoor_deviceID": "DELCPCB005",
            "contact_person": "Mr. Abhishek Jain",
            "contact_number": "9990333248",
            "emailID": "abhishek@edsglobal.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "850",
            "occupancy": "3",
            "created_on": "2024-09-25 07:21:43",
            "updated_on": "2024-09-25 07:21:43"
        },
        {
            "deviceID": "1201240074",
            "deployementID": "RESF-008",
            "typology": "Residential",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Living Room",
            "installation_date": "2024-03-18 00:00:00",
            "uninstallation_date": null,
            "address": "F-5, 318-N, Chirag Delhi, Delhi-110017",
            "latitude": "28.536",
            "longitude": "77.225",
            "nearby_AQI_station": "SiriFort, Delhi-CPCB (2 Kms)",
            "outdoor_deviceID": "DELCPCB005",
            "contact_person": "Mr. Abhishek Jain",
            "contact_number": "9990333248",
            "emailID": "abhishek@edsglobal.com",
            "total_no_of_floors": "5",
            "installation_floor_no": "1",
            "total_build_up_area_sq_m": "850",
            "occupancy": "3",
            "created_on": "2024-07-18 11:04:32",
            "updated_on": "2024-07-18 11:04:32"
        },
        {
            "deviceID": "1203240077",
            "deployementID": "REWZ - 21",
            "typology": "Apartment",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom",
            "installation_date": "2024-05-05 00:00:00",
            "uninstallation_date": null,
            "address": "B-2/51-A, Keshav Puram",
            "latitude": "28.684",
            "longitude": "77.1605",
            "nearby_AQI_station": "Delhi-35",
            "outdoor_deviceID": "DELDPCC014",
            "contact_person": "Gurneet Singh",
            "contact_number": "9899240140",
            "emailID": "gurneet.singh@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "0",
            "total_build_up_area_sq_m": "110",
            "occupancy": "4",
            "created_on": "2024-09-30 04:55:51",
            "updated_on": "2024-09-30 04:55:51"
        },
        {
            "deviceID": "1203240082",
            "deployementID": "REWZ - 22",
            "typology": "Apartment",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": "Bedroom - Prabhansh Room",
            "installation_date": "2024-05-05 00:00:00",
            "uninstallation_date": null,
            "address": "B-2/51-A, Keshav Puram",
            "latitude": "28.6839",
            "longitude": "77.1604",
            "nearby_AQI_station": "Delhi-35",
            "outdoor_deviceID": "DELDPCC014",
            "contact_person": "Gurneet Singh",
            "contact_number": "9899240140",
            "emailID": "gurneet.singh@gmail.com",
            "total_no_of_floors": "4",
            "installation_floor_no": "0",
            "total_build_up_area_sq_m": "110",
            "occupancy": "4",
            "created_on": "2024-09-30 04:56:00",
            "updated_on": "2024-09-30 04:56:00"
        },
        {
            "deviceID": "1202240029",
            "deployementID": "SCD8-017",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-27 00:14:07",
            "uninstallation_date": null,
            "address": "St. Mary's School, Dwarka Sec-19",
            "latitude": "28.5749",
            "longitude": "77.049",
            "nearby_AQI_station": "Dwarka Sec-8",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Mrs. Reena Khurana",
            "contact_number": "9811349418",
            "emailID": "reenakhuhrana415@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "25900",
            "occupancy": "40",
            "created_on": "2024-09-16 05:21:05",
            "updated_on": "2024-09-16 05:21:05"
        },
        {
            "deviceID": "1202240028",
            "deployementID": "SCD8-020",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-29 00:14:07",
            "uninstallation_date": null,
            "address": "St. Mary's School, Dwarka Sec-19",
            "latitude": "28.5748",
            "longitude": "77.0489",
            "nearby_AQI_station": "Dwarka Sec-8",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Mrs. Reena Khurana",
            "contact_number": "9811349418",
            "emailID": "reenakhuhrana415@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "25900",
            "occupancy": "45",
            "created_on": "2024-09-16 05:21:14",
            "updated_on": "2024-09-16 05:21:14"
        },
        {
            "deviceID": "1202240010",
            "deployementID": "SCD8-18",
            "typology": "Office",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-27 00:14:07",
            "uninstallation_date": null,
            "address": "St. Mary's School, Dwarka Sec-19",
            "latitude": "28.5749",
            "longitude": "77.049",
            "nearby_AQI_station": "Dwarka Sec-8",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Mrs. Reena Khurana",
            "contact_number": "9811349418",
            "emailID": "reenakhuhrana415@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "-1",
            "total_build_up_area_sq_m": "25900",
            "occupancy": "50",
            "created_on": "2024-09-16 05:21:19",
            "updated_on": "2024-09-16 05:21:19"
        },
        {
            "deviceID": "1202240012",
            "deployementID": "SCD8-19",
            "typology": "School",
            "active": "1",
            "primary_sensor": "1",
            "spaceType": null,
            "installation_date": "2024-03-29 00:14:07",
            "uninstallation_date": null,
            "address": "St. Mary's School, Dwarka Sec-19",
            "latitude": "28.5748",
            "longitude": "77.0489",
            "nearby_AQI_station": "Dwarka Sec-8",
            "outdoor_deviceID": "DELDPCC016",
            "contact_person": "Mrs. Reena Khurana",
            "contact_number": "9811349418",
            "emailID": "reenakhuhrana415@gmail.com",
            "total_no_of_floors": "2",
            "installation_floor_no": "2",
            "total_build_up_area_sq_m": "25900",
            "occupancy": "20",
            "created_on": "2024-07-18 11:04:41",
            "updated_on": "2024-07-18 11:04:41"
        }
    ]
}
    ]
}
"""

# Function to extract device details from the raw text
def extract_device_details(device_id, device_info_text):
    try:
        data = json.loads(device_info_text)  # Parse the text as JSON
        devices = data.get("Data", [])
        
        # Find the device by device_id
        device_info = next((item for item in devices if item["deviceID"] == device_id), None)
        
        if device_info:
            address = device_info.get("address", "NaN")
            typology = device_info.get("typology", "NaN")
            return address, typology
        else:
            return "NaN", "NaN"
    except json.JSONDecodeError:
        return "Error", "Error"

# Function to plot and display heatmaps in Streamlit
def plot_and_display_feature_heatmaps(df, features, year, month):
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

    # Filter data for the selected month
    for feature in features:
        indoor_feature = feature

        # Filter data for the current feature and year
        feature_data = df[(df.index.year == year) & (df.index.month == month)][feature]

        if feature_data.empty:
            st.warning(f"No data available for {feature} in {calendar.month_name[month]} {year}.")
            continue

        # Initialize the figure for a single subplot (for a single month)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Define custom color map
        color_list = ['#006400', '#228B22', '#FFFF00', '#FF7F00', '#FF0000', '#8B0000']
        cmap = ListedColormap(color_list)

        # Get boundaries and labels for the feature
        boundaries = feature_boundaries[feature]
        labels = feature_labels[feature]

        # Adjust boundaries to avoid extra tick issue
        if len(boundaries) - 1 != len(labels):
            labels = labels[:-1]  # Adjust if boundaries and labels lengths don't match

        # Prepare the calendar data (up to 5 weeks in a month)
        num_days = calendar.monthrange(year, month)[1]
        calendar_data = np.full((5, 7), np.nan)  # 5 rows to accommodate up to 5 weeks

        for day in range(1, num_days + 1):
            day_values = feature_data[feature_data.index.day == day]
            if not day_values.empty:
                daily_avg = day_values.mean()

                # Calculate position in the calendar grid
                first_day_of_month = calendar.monthrange(year, month)[0]  # First weekday of the month
                week_row = (day + first_day_of_month - 1) // 7
                week_col = (day + first_day_of_month - 1) % 7

                # Ensure the week_row is within bounds (maximum of 5 rows)
                if week_row < 5:
                    calendar_data[week_row, week_col] = daily_avg

        # Plot the heatmap for the selected feature
        norm = BoundaryNorm(boundaries, cmap.N)
        sns.heatmap(calendar_data, annot=True, fmt=".0f", cmap=cmap, norm=norm,
                    cbar=False, xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 
                    yticklabels=[1, 2, 3, 4, 5], ax=ax, linewidths=1, linecolor='black')

        ax.set_title(f"{calendar.month_name[month]} {year} - {indoor_feature}", fontsize=14)
        ax.set_xlabel("Day of the Week", fontsize=12)
        ax.set_ylabel("Week", fontsize=12)

        # Create extra space for the color bar and adjust layout
        fig.subplots_adjust(right=0.85)  # Add more space to the right of the subplots

        # Create the color bar in the extra space to the right
        cbar_ax = fig.add_axes([0.87, 0.1, 0.03, 0.8])  # Position for the color bar
        cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax, orientation='vertical')

        # Set color bar ticks and labels
        cbar.set_ticks([(b + b_next) / 2 for b, b_next in zip(boundaries[:-1], boundaries[1:])])
        cbar.set_ticklabels(labels)
        cbar.ax.tick_params(labelsize=12)  # Adjust font size of color bar ticks
        cbar.ax.set_ylabel(f"{feature} Levels", fontsize=14)  # Label for the color bar

        # Display the heatmap in Streamlit
        st.pyplot(fig)
        plt.close()

# Streamlit app
st.title("CABH Indoor Air Quality Monitoring")

# User inputs
device_id = st.text_input("Enter Device ID:", value="1201240075")
year = st.number_input("Select Year:", min_value=2024, max_value=2025, value=2024)
month = st.selectbox("Select Month:", list(range(1, 13)))

# Button to generate heatmaps
if st.button("Generate Heatmaps"):
    if not device_id.strip():
        st.error("Device ID cannot be empty.")
        st.stop()

    # Extract device details from raw text
    address, typology = extract_device_details(device_id, device_info_text)

    # Display the extracted details
    st.subheader(f"Device ID: {device_id}")
    st.write(f"Address: {address}")
    st.write(f"Typology: {typology}")

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
