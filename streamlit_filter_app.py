import streamlit as st
import pandas as pd

# Function to upload CSV file
def upload_csv():
    st.title("Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV:")
        st.write(data)
        st.session_state.data = data
        st.success("File uploaded successfully!")
        st.button("Next: Selection of Patients", on_click=show_selection)

# Function to display selection of patients UI
def show_selection():
    st.title("Selection of Patients")
    if "data" not in st.session_state:
        st.warning("Please upload a CSV file first.")
        return
    data = st.session_state.data

    # Filter options
    st.subheader("Filter Options:")
    selected_column = st.selectbox("Select a column to filter:", data.columns)
    unique_values = data[selected_column].unique()
    selected_value = st.selectbox("Select a value to filter by:", unique_values)
    filtered_data = data[data[selected_column] == selected_value]

    # Display filtered CSV
    st.write("Filtered CSV:")
    st.write(filtered_data)

    # Analyze patients button
    if st.button("Analyze Patients"):
        st.session_state.filtered_data = filtered_data
        st.experimental_rerun()

# Function to evaluate results
def evaluate_results():
    st.title("Evaluate Results")
    if "filtered_data" not in st.session_state:
        st.warning("Please filter the data first.")
        return
    filtered_data = st.session_state.filtered_data

    # Display each entry in the CSV
    st.write("Edited CSV:")
    edited_data = filtered_data.copy()
    for index, row in edited_data.iterrows():
        for column in edited_data.columns:
            new_value = st.text_input(f"Edit {column} for index {index}:", value=row[column])
            edited_data.at[index, column] = new_value

    # Export edited CSV
    if st.button("Export Edited CSV"):
        st.write(edited_data)
        st.balloons()
        st.button("Start Over", on_click=upload_csv)

# Main function to run the application
def main():
    st.set_page_config(page_title="Healthcare Admin Application")

    # Check which window to display
    if "selection" in st.session_state:
        if st.session_state.selection:
            show_selection()
        else:
            evaluate_results()
    else:
        upload_csv()

if __name__ == "__main__":
    main()
