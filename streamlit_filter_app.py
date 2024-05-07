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
            
    if len(filtered_data) > 0:
            index = 0
            show_entry = True
            while show_entry:
                # Display current row
                st.write(f"Entry {index + 1} of {len(filtered_data)}:")
                st.write(filtered_data.iloc[index])

                # Navigation buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                if col2.button("Next"):
                    index = (index + 1) % len(filtered_data)
                if col1.button("Previous"):
                    index = (index - 1) % len(filtered_data)

                # Check if end of dataframe reached
                if index == len(filtered_data) - 1:
                    col2.write("End of entries")
                show_entry = col2.button("Show next entry", key="show_next")


def main():
    st.title("Healthcare Admin Application")

    # First window: Upload CSV
    uploaded_data = upload_csv()

    # Second window: Selection of Patients
    if uploaded_data is not None:
        # Explicitly convert all columns to string type
        uploaded_data = uploaded_data.astype(str)
        select_patients(uploaded_data)

if __name__ == "__main__":
    main()
