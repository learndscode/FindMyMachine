import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import reverse_geocoder as rg

from geolocate import get_location

st.set_page_config(
    page_title="Find My Machines",
    page_icon="assets/SkidSteer.png",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

st.title("Find My Machines")

upload_file = st.file_uploader("Choose a spreadsheet file", type="xlsx")

if upload_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(upload_file, engine='openpyxl')
    # Replace NaN with None across entire DataFrame
    #df = df.apply(lambda col: col.map(lambda x: None if pd.isna(x) else x))
    df = df.fillna("None")

    st.subheader("Data Summary")
    st.write("Total records uploaded: " + str(f"{len(df):,}"))

    #if st.button("Compare Locations"):
        # Apply reverse geocoding
    df[['City', 'State', 'Country']] = df.apply(
        lambda row: get_location(row['Latitude'], row['Longitude']), axis=1)
    df = df.fillna("None")
    st.subheader("Filter Data")
    # Add 'All' option to the list
    columns = df.columns.to_list()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = ['All'] + sorted(df[selected_column].unique())
    selected_value = st.selectbox("Select value", unique_values)
    
    # Filter logic
    if selected_value == 'All':
        filtered_df = df
    else:
        filtered_df = df[df[selected_column] == selected_value]
    st.write("Total records selected: " + str(f"{len(filtered_df):,}"))
    st.write(filtered_df)
else:
    st.write("Waiting on  file upload...")
