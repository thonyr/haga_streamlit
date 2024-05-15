import streamlit as st
import pandas as pd
import numpy as np

# Static variables that are going to be retrieved from the real data
DUMMY_NR_OF_PATIENTS = 1000

# Function to process CSV data
def process_csv(file):
    df = pd.read_csv(file, delimiter=';')
    df_sorted = df.sort_values(by=['predicted_switch','revenue_difference'], ascending=False)
    df_sorted['evaluated_by_doctor'] = False  # Add a column to track evaluation
    st.session_state.available_time = len(df_sorted) / 60
    return df_sorted

# Main function for Streamlit app
def main():
    st.markdown(
        """
        <style>
        .main {
            max-width: 1800px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display the image and title
    col1, col2 = st.columns([3, 3])
    with col1:
        st.image("haga.png")
    with col2:
        st.markdown("# Cardiologie onderregistratie")
    
    
    # Initialize session state
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None
    if 'current_index' not in st.session_state:
        st.session_state.current_index = None
    if 'auto_next' not in st.session_state:
        st.session_state.auto_next = False
    if 'session_ended' not in st.session_state:
        st.session_state.session_ended = False
    if 'page' not in st.session_state:
        st.session_state.page = 0

    # Page 1: Getting the CSV
    if st.session_state.page == 0:
        st.subheader('Upload data-bestand')
        st.write('Upload een CSV met patientenbestand om te beginnen, of gebruik dummy data.')

        use_dummy = st.button("Use Dummy Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if use_dummy:
            try:
                dummy_file_path = 'fake_dataset_2.csv'
                st.session_state.filtered_df = process_csv(dummy_file_path)
                st.session_state.page = 1
                st.rerun()
            except FileNotFoundError:
                st.error("Dummy file 'fake_dataset_2.csv' not found.")
        elif uploaded_file is not None:
            st.session_state.filtered_df = process_csv(uploaded_file)
            st.session_state.page = 1
            st.rerun()

    # Page 2: Summary and Time Slider
    elif st.session_state.page == 1:
        if st.session_state.filtered_df is not None:
            st.subheader('Geef beschikbare tijd aan:')

            available_time = st.slider(
                "How much time do you have? (in hours)",
                min_value=1,
                max_value=int(len(st.session_state.filtered_df) / 60),
                value=int(st.session_state.available_time)  # Set default value to session state available time
            )

            if available_time != st.session_state.available_time:
                st.session_state.available_time = available_time
                st.rerun()

            st.write("---")
            

            nr_patients_within_time = int(st.session_state.available_time * 60)  # Ensure this is an integer
            st.write(f"Number of Patients: **{nr_patients_within_time}**")
            st.write(f"Verwachte tijd om te controleren: **{round(st.session_state.available_time,1)} uur**")
            
            # Sum the product of 'revenue_difference' and 'dbc_switch' for the first 'nr_patients_within_time' entries
            sum_revenue_difference = (st.session_state.filtered_df.iloc[:nr_patients_within_time]['revenue_difference'] * 
                                    st.session_state.filtered_df.iloc[:nr_patients_within_time]['dbc_switch']).sum()

            st.write(f"Totale opbrengst voor geselecteerde patiënten: **€{sum_revenue_difference:,.2f}**")

            st.write(f"Gemiddeld opbrengstverschil per uur: **€{sum_revenue_difference / st.session_state.available_time:,.2f}**")

            # Number of full DBC codes in the first nr_patients_within_time
            percentage_full_patients = round(st.session_state.filtered_df['full'].iloc[:nr_patients_within_time].mean() * 100, 2)
            st.write(f"Percentage of patients with full DBC codes: **{percentage_full_patients}%**")

            average_count_score = round(st.session_state.filtered_df['count_score'].iloc[:nr_patients_within_time].mean(), 2)
            st.write(f"Average count score for {nr_patients_within_time} patients: **{average_count_score}**")

            average_switch_percentage = round(st.session_state.filtered_df['full'].iloc[:nr_patients_within_time].mean() * 100, 2)
            st.write(f"Gemiddeld aantal volle dbc's: **{average_switch_percentage}%**")

            if st.button('Evalueer de notities'):
                st.session_state.page = 2
                st.rerun()

    # Page 3: Analyze with Language Model
    elif st.session_state.page == 2:
        
        if st.session_state.filtered_df is not None:
            if st.session_state.current_index is None:
                st.session_state.current_index = 0

            st.subheader('Analyse resultaten:')

            current_row = st.session_state.filtered_df.iloc[st.session_state.current_index]

            # Mark the current record as evaluated
            st.session_state.filtered_df.at[current_row.name, 'evaluated_by_doctor'] = True

            # Create a DataFrame with only the values
            values_data = {
                'Value': [
                    "<B>Patientnummer:</B> " + str(current_row['patient_id']),
                    "<B>Datum consult:</B> " + str(current_row['consult_date_zorg_activiteiten']),
                    current_row['naslag_report_content'],
                    "<B>Uitleg taalmodel:</B> " + str(current_row['opmerkingen']),
                    "<B>Huidige DBC-code:</B> " + str(current_row['dbc_diagnosis_code']),
                    "<B>Gecorrigeerde code: </B> " + str(st.session_state.filtered_df.loc[current_row.name, 'corrected_dbc'])
                ]
            }

            df_values = pd.DataFrame(values_data).reset_index(drop=True)

            # Create a markdown table with line breaks, using a dummy header for structure
            markdown_table = "|  |\n| --- |\n"
            for val in df_values['Value']:
                markdown_table += f"| {str(val).replace('\n', '<br>')} |\n"

            # Display the markdown table
            st.markdown(markdown_table, unsafe_allow_html=True)

            # Add space before navigation buttons
            st.write("")

            # Input for corrected DBC code
            corrected_dbc = st.text_input('Corrected DBC Code', str(current_row['corrected_dbc']))

            # Update DataFrame and session state with the new corrected_dbc value
            if corrected_dbc != str(current_row['corrected_dbc']):
                try:
                    corrected_dbc_int = int(corrected_dbc)
                except ValueError:
                    corrected_dbc_int = corrected_dbc

                st.session_state.filtered_df.loc[current_row.name, 'corrected_dbc'] = corrected_dbc_int

                if st.session_state.auto_next:
                    if st.session_state.current_index < len(st.session_state.filtered_df) - 1:
                        st.session_state.current_index += 1
                    st.rerun()

            # Add a checkbox for auto-next feature
            st.session_state.auto_next = st.checkbox('Automatisch volgende notitie bij wijziging DBC', value=st.session_state.auto_next)

            # Show the current record and total records
            st.write(f"Record {st.session_state.current_index + 1} van {len(st.session_state.filtered_df)}")

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                if st.button('Previous') and st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.rerun()

            with col3:
                if st.button('Next') and st.session_state.current_index < len(st.session_state.filtered_df) - 1:
                    st.session_state.current_index += 1
                    st.rerun()

            # End session button
            if not st.session_state.session_ended:
                if st.button('End session'):
                    st.session_state.session_ended = True
                    st.session_state.page = 3
                    st.rerun()

    # Page 4: Session Ended and Summary
    elif st.session_state.page == 3:
        evaluated_records = st.session_state.filtered_df[st.session_state.filtered_df['evaluated_by_doctor']]
        
        st.subheader("Evaluatie huidige sessie")
        st.write(f"Sessie beëindigd. Aantal geëvalueerde records: **{len(evaluated_records)}**")
        st.write(f'Aantal gewijzigde DBC-codes: **{evaluated_records["dbc_diagnosis_code"].eq(evaluated_records["corrected_dbc"]).sum()}**')

        total_revenue_difference = evaluated_records[evaluated_records['dbc_diagnosis_code'] != evaluated_records['corrected_dbc']]['revenue_difference'].sum()
        st.write(f"Totaal revenue difference van geëvalueerde records: **€{total_revenue_difference:,.2f}**")
        
        # Display download button
        csv = evaluated_records.to_csv(index=False)
        st.download_button(
            label="Download resultaten",
            data=csv,
            file_name='evaluated_data.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
