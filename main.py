import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import reverse_geocoder as rg
import base64

from geolocate import get_location, review_needed, highlight_cells

st.set_page_config(
    page_title="Find My Machines",
    page_icon="assets/SkidSteer.png",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

# Path to your image in the assets folder
image_path = "assets/SkidSteer.png"

# Encode image to base64
with open(image_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Inject HTML with inline image and title (vertically aligned)
st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{encoded}" width="60" style="margin-right: 15px;" />
        <h1 style="margin: 0;">Find My Machine</h1>
    </div>
""", unsafe_allow_html=True)

upload_file = st.file_uploader("Choose a spreadsheet file to upload.", type="xlsx")

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
    df.replace('', None, inplace=True)
    # Reorder columns to have Country, State, City first
    df = df.fillna("None")
    df['Needs Review'] = "No"
    df['Needs Review'] = df.apply(review_needed, axis=1)
    # Reorder columns to have Country, State, City first
    columns =['Needs Review'] + [col for col in df.columns if col not in ['Needs Review', 'Country', 'State', 'City']] + ['Country', 'State', 'City']
    df = df[columns]

    st.subheader("Filter Data")
    # Add 'All' option to the list
    columns = df.columns.to_list()
    selected_column = st.selectbox("Select column to filter by", columns)
    if selected_column == "Needs Review":
        unique_values = ['All', 'Yes', 'No']
    else:
        unique_values = ['All'] + sorted(df[selected_column].unique())
    selected_value = st.selectbox("Select value", unique_values)

    # Filter logic
    if selected_value == 'All':
        filtered_df = df
    else:
        filtered_df = df[df[selected_column] == selected_value]

    # Dataframe styling
    # Apply the styling
    #styled_df = filtered_df.style.applymap(color_needs_review, subset=['Needs Review'])
    styled_df = filtered_df.style.apply(highlight_cells, axis=1)

    st.write("Total records selected: " + str(f"{len(filtered_df):,}"))
    st.write(styled_df)
else:
    st.write("Waiting on  file upload...")
