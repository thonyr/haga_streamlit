import streamlit as st
import pandas as pd

def filter_data(df, column1, column2, filter1, filter2):
    filtered_df = df[(df[column1] == filter1) & (df[column2] == filter2)]
    return filtered_df

def main():
    st.title('Streamlit Table Filtering App')

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write("## Original Data")
        st.write(df)

        st.sidebar.title('Filter Data')

        column1 = st.sidebar.selectbox('Select Column 1', df.columns)
        column2 = st.sidebar.selectbox('Select Column 2', df.columns)

        unique_values_column1 = df[column1].unique()
        unique_values_column2 = df[column2].unique()

        filter_value1 = st.sidebar.selectbox('Select Value for Column 1', unique_values_column1)
        filter_value2 = st.sidebar.selectbox('Select Value for Column 2', unique_values_column2)

        filtered_df = filter_data(df, column1, column2, filter_value1, filter_value2)

        st.write("## Filtered Data")
        st.write(filtered_df)

if __name__ == '__main__':
    main()
