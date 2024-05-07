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

    # Analyze Data button
    if st.button("Analyze Data"):
        analyze_data(filtered_data)

def analyze_data(filtered_data):
    st.title("Analysis of Patient Data")
    if not hasattr(analyze_data, "index"):
        analyze_data.index = 0

    if len(filtered_data) == 0:
        st.warning("No data to analyze.")
        return

    current_row = filtered_data.iloc[analyze_data.index]

    st.write("Selected Fields:")
    st.write("Medical Note:", current_row["db_cs_afgelopen_jaar_dbc_diagnosis_code_description"])
    st.write("Current DBC:", current_row["dbc_diagnosis_code"])

    # Next and Back buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    if col2.button("Back") and analyze_data.index > 0:
        analyze_data.index -= 1
    if col2.button("Next") and analyze_data.index < len(filtered_data) - 1:
        analyze_data.index += 1

def main():
    st.title("Healthcare Admin Application")

    # First window: Upload CSV
    uploaded_data = upload_csv()

    # Second window: Selection of Patients
    if uploaded_data is not None:
        select_patients(uploaded_data)

if __name__ == "__main__":
    main()
