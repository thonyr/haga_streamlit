import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate average of a column
def calculate_average(column):
    return np.mean(column)

# Function to generate random placeholder values
def generate_placeholder():
    return np.random.randint(1, 15)

# Function to process uploaded CSV file
def process_csv(file):
    df = pd.read_csv(file)
    num_entries = len(df)
    average_revenue_difference = calculate_average(df['revenue_difference'])
    average_switch_change = generate_placeholder()
    dbc_full_percentage = generate_placeholder()
    average_count_score = generate_placeholder()
    return num_entries, average_revenue_difference, average_switch_change, dbc_full_percentage, average_count_score

# Main function for Streamlit app
def main():
    st.title('CSV Analyzer App')
    st.write('Upload a CSV file to analyze')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        num_entries, avg_revenue_diff, avg_switch_change, dbc_full_percentage, avg_count_score = process_csv(uploaded_file)

        # Display basic statistics about the uploaded CSV file
        st.write("Basic Statistics:")
        stats_data = {
            'Statistic': ['Number of Patients', 'Average Revenue Difference', 'Average Change of Switch', 'DBC Full Percentage', 'Average Count Score'],
            'Value': [
                num_entries,
                avg_revenue_diff,
                avg_switch_change,
                dbc_full_percentage,
                avg_count_score
            ]
        }
        st.table(pd.DataFrame(stats_data).style.set_properties(**{'font-weight': 'bold'}))

        # Continue with existing functionality
        available_time = st.slider("How much time do you have? (in hours)", 0, 12, 5)

        if st.button('Select Patients'):
            filtered_df = process_csv(uploaded_file)
            st.session_state.current_index = 0
            current_row = filtered_df.iloc[st.session_state.current_index]
            table_data = {
                'Field': ['Naslag Report Content', 'DBC Diagnosis Code', 'Consult Date Zorg Activiteiten', 'Corrected DBC', 'DBC Switch'],
                'Value': [
                    current_row['naslag_report_content'],
                    current_row['dbc_diagnosis_code'],
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
            if col3.button('Next') and st.session_state.current_index < len(filtered_df) - 1:
                st.session_state.current_index += 1

            # Save button
            if st.button('Save'):
                filtered_df.at[st.session_state.current_index, 'dbc_diagnosis_code'] = table_data['Value'][1]

            # Export to CSV button
            if st.button('Export to CSV'):
                export_df = filtered_df[['naslag_report_content', 'dbc_diagnosis_code', 'consult_date_zorg_activiteiten', 'corrected_dbc', 'dbc_switch']]
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='filtered_data.csv',
                    mime='text/csv'
                )

if __name__ == '__main__':
    main()
