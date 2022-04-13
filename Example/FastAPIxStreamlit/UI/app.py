import streamlit as st
import requests
import pandas as pd
from  pandasql import sqldf
from utils import *


def main():
    st.set_page_config(page_title="Tabular data QA")
    st.sidebar.title("GPT for SQL")
    
    model = st.sidebar.selectbox(
            'Select model version',
            ('baseline',))
    
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        if (uploaded_file.name.split('.')[-1] == "csv"):
            df = pd.read_csv(uploaded_file, encoding = "ISO-8859-1")
        else:
            df = pd.read_excel(uploaded_file)


        # Change columns to snake style
        columns = df.columns
        columns = [camel_to_snake(i) for i in columns]
        df.columns = columns
        
        datatypes = df.dtypes
        schema_dict = dict(zip(columns, datatypes))

        # Get columns selection from user
        columns_selection = st.sidebar.multiselect(
            'Select columns that you want to query', columns , 
            default = list(columns[:3]),      
        )
        
        
        # Show user dataset
        dataframe = st.dataframe(df)

        # User enter question
        question = st.text_input(
            label='Enter your question',
            value='',
        )
        
        button = st.button('Ask')

        if button:
            if (checkColumns(columns_selection)):


                settings = {
                    "temperature" : 0.7,
                    "num_beams" : 10,
                    "top_p" : 0.8,
                    "top_k" : 100,
                    "model_ver" : model
                }

                # Get schema example : (col : type)
                selected_dict = {i : schema_dict[i] for i in schema_dict.keys() if i in columns_selection}


                # Get SQL
                result = get_answer(data=selected_dict , question= question, settings= settings)
                result = result.replace('TABLE' , 'df')

                # Show SQL result
                st.code(result, language="sql")
                
                try:
                    # Execute SQL and display result
                    temp_df = sqldf(result)
                    dataframe = st.dataframe(temp_df)
                    correct = True
                except Exception as e:
                    st.warning(e)
                    correct = False
                saveLogs(uploaded_file.name , columns_selection , question , result, model , correct) 


if __name__ == '__main__':
    main()
