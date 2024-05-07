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
    for column in selected_columns:
        unique_values = data[column].unique()
        selected_value = st.selectbox(f"Select {column}", unique_values)
        data = data[data[column] == selected_value]

    st.write("Filtered Data:")
    st.dataframe(data)

def main():
    st.title("Healthcare Admin Application")

    # First window: Upload CSV
    uploaded_data = upload_csv()

    # Second window: Selection of Patients
    if uploaded_data is not None:
        select_patients(uploaded_data)

if __name__ == "__main__":
    main()
