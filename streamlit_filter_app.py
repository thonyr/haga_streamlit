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
    
    average_revenue_difference = calculate_average(filtered_df['revenue_difference'])
    average_switch_change = generate_placeholder()
    dbc_full_percentage = generate_placeholder()
    average_count_score = generate_placeholder()
    
    return num_filtered_entries, average_revenue_difference, average_switch_change, dbc_full_percentage, average_count_score

# Main function for Streamlit app
def main():
    st.title('CSV Analyzer App')
    st.write('Upload a CSV file to analyze')
    available_time = st.slider("How much time do you have? (in hours)", 0, 12, 5)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        num_entries, avg_revenue_diff, avg_switch_change, dbc_full_percentage, avg_count_score = process_csv(uploaded_file, available_time)

        st.write(f"Number of Patients: {num_entries}")
        st.write(f"Average Revenue Difference: {avg_revenue_diff}")
        st.write(f"Average Change of Switch: {avg_switch_change}")
        st.write(f"DBC Full Percentage: {dbc_full_percentage}")
        st.write(f"Average Count Score: {avg_count_score}")

if __name__ == '__main__':
    main()
