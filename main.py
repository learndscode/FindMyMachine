import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.read_excel(upload_file)

    st.subheader("Data Summary")
    st.write("Total records uploaded: " + str(f"{len(df):,}"))

    if st.button("Compare Locations"):
        st.subheader("Filter Data")
        columns = df.columns.to_list()
        selected_column = st.selectbox("Select column to filter by", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value", unique_values)

        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)
else:
    st.write("Waiting on  file upload...")
