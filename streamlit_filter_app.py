import streamlit as st
import pandas as pd

# Function to upload CSV file
def upload_csv():
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data

# Function to display selection of patients
def select_patients(data):
    st.title("Selection of Patients")
    st.dataframe(data)

    # Filter by column headers
    selected_columns = st.multiselect("Select Columns", data.columns)

    # Filter by column values
    filtered_data = data
    for column in selected_columns:
        unique_values = data[column].unique()
        selected_values = st.multiselect(f"Select {column}", unique_values)
        filtered_data = filtered_data[filtered_data[column].isin(selected_values)]

    st.write("Filtered Data:")
    st.dataframe(filtered_data)

    # Analyse data button
    if st.button("Analyse data"):
        if len(filtered_data) > 0:
            analyze_data(filtered_data)

# Function to analyze each entry in filtered data
def analyze_data(filtered_data):
    st.title("Analysis of Data")
    idx = 0
    total_entries = len(filtered_data)

    # Circular scrolling
    while True:
        entry = filtered_data.iloc[idx]
        st.write(f"Entry {idx+1} of {total_entries}")
        st.write(entry)

        # Next and previous buttons
        if st.button("Next", key="next_button"):
            idx = (idx + 1) % total_entries
        if st.button("Previous", key="prev_button"):
            idx = (idx - 1) % total_entries

def main():
    st.title("Healthcare Admin Application")

    # First window: Upload CSV
    uploaded_data = upload_csv()

    # Second window: Selection of Patients
    if uploaded_data is not None:
        select_patients(uploaded_data)

if __name__ == "__main__":
    main()
