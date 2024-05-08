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
        filtered_df = process_csv(uploaded_file, available_time)

        # Initialize current index
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0

        # Display current entry
        st.write("Filtered Data:")
        current_row = filtered_df.iloc[st.session_state.current_index]
        st.write(f"Patient {st.session_state.current_index + 1}:")
        st.write(f"Naslag Report Content: {current_row['naslag_report_content']}")
        st.write(f"DBC Diagnosis Code: {current_row['dbc_diagnosis_code']}")
        st.write(f"Consult Date Zorg Activiteiten: {current_row['consult_date_zorg_activiteiten']}")
        st.write(f"Corrected DBC: {current_row['corrected_dbc']}")
        st.write(f"DBC Switch: {current_row['dbc_switch']}")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        if col2.button('Previous') and st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        if col3.button('Next') and st.session_state.current_index < len(filtered_df) - 1:
            st.session_state.current_index += 1

if __name__ == '__main__':
    main()
