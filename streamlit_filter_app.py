import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate time required to check the CSV
def calculate_time(num_entries):
    total_hours = (num_entries / 1000) * 10
    return total_hours

# Function to calculate the number of entries based on user-defined time
def calculate_entries(num_entries, available_time):
    total_hours = calculate_time(num_entries)
    if total_hours <= available_time:
        return num_entries
    else:
        return int((available_time / total_hours) * num_entries)

# Function to calculate average of a column
def calculate_average(column):
    return np.mean(column)

# Function to generate random placeholder values
def generate_placeholder():
    return np.random.randint(1, 15)

# Function to process uploaded CSV file
def process_csv(file, available_time):
    df = pd.read_csv(file)
    num_entries = len(df)
    num_filtered_entries = calculate_entries(num_entries, available_time)
    
    # Sorting the dataframe based on revenue_difference
    df_sorted = df.sort_values(by='revenue_difference', ascending=False)
    
    filtered_df = df_sorted.head(num_filtered_entries)
    
    return filtered_df

# Main function for Streamlit app
def main():
    st.title('CSV Analyzer App')
    st.write('Upload a CSV file to analyze')
    available_time = st.slider("How much time do you have? (in hours)", 0, 12, 5)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        if st.button('Select Patients'):
            filtered_df = process_csv(uploaded_file, available_time)
            st.write("Filtered Data:")
            for index, row in filtered_df.iterrows():
                st.write(f"Patient {index+1}:")
                st.write(f"Naslag Report Content: {row['naslag_report_content']}")
                st.write(f"DBC Diagnosis Code: {row['dbc_diagnosis_code']}")
                st.write(f"Consult Date Zorg Activiteiten: {row['consult_date_zorg_activiteiten']}")
                st.write(f"Corrected DBC: {row['corrected_dbc']}")
                st.write(f"DBC Switch: {row['dbc_switch']}")
                st.write("---")

if __name__ == '__main__':
    main()
