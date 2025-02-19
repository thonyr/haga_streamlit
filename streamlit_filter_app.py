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

# Function to process uploaded CSV file
def process_csv(file, available_time):
    df = pd.read_csv(file)
    num_entries = len(df)
    num_filtered_entries = calculate_entries(num_entries, available_time)
    
    # Sorting the dataframe based on revenue_difference
    df_sorted = df.sort_values(by='revenue_difference', ascending=False)
    
    filtered_df = df_sorted.head(num_filtered_entries)
    
    return filtered_df

# Function to generate random percentages
def generate_random_percentages():
    return {
        'avg. chance of switch': np.random.uniform(0, 100),
        'DBC full percent': np.random.uniform(0, 100)
    }

# Main function for Streamlit app
def main():
    st.title('HagaZiekenhuis Healthcare Administration App')
    st.write('Upload a CSV file to analyze')
    available_time = st.slider("How much time do you have? (in hours)", 0, 12, 5)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        filtered_df = process_csv(uploaded_file, available_time)

        # Additional pane displaying values
        st.sidebar.title('Additional Information')
        st.sidebar.subheader('Statistics:')
        st.sidebar.write(f"Number of Patients: {len(filtered_df)}")
        st.sidebar.write(f"Average Revenue Difference: {filtered_df['revenue_difference'].mean()}")

        # Random percentages
        st.sidebar.subheader('Random Percentages:')
        random_percentages = generate_random_percentages()
        for field, value in random_percentages.items():
            st.sidebar.write(f"{field}: {value:.2f}%")

        # Initialize current index
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
            st.session_state.filtered_df = filtered_df  # Store the filtered DataFrame in session state

        # Display current entry in tabulated format
        st.write("Filtered Data:")
        current_row = st.session_state.filtered_df.iloc[st.session_state.current_index]
        dbc_diagnosis_code = st.text_input('DBC Diagnosis Code', str(current_row['dbc_diagnosis_code']))  # Ensure it's a string
        st.session_state.filtered_df.loc[current_row.name, 'dbc_diagnosis_code'] = int(dbc_diagnosis_code)  # Explicitly cast to int

        table_data = {
            'Field': ['Naslag Report Content', 'DBC Diagnosis Code', 'Consult Date Zorg Activiteiten', 'Corrected DBC', 'DBC Switch'],
            'Value': [
                current_row['naslag_report_content'],
                dbc_diagnosis_code,
                current_row['consult_date_zorg_activiteiten'],
                current_row['corrected_dbc'],
                current_row['dbc_switch']
            ]
        }
        st.table(pd.DataFrame(table_data).style.set_properties(**{'font-weight': 'bold'}))

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        if col2.button('Previous') and st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        if col3.button('Next') and st.session_state.current_index < len(st.session_state.filtered_df) - 1:
            st.session_state.current_index += 1

        # Export to CSV button
        if st.button('Export to CSV'):
            csv = st.session_state.filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv'
            )

if __name__ == '__main__':
    main()
