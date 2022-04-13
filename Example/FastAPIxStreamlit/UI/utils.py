import re
import requests
import streamlit as st

def checkColumns(selected):
    if (len(selected) < 1 or len(selected) > 10):
        st.error("Number of column from 1 to 10")
        return False
    return True

def saveLogs(filename , columns, question, result, model, correct):
    with open('log.txt' , 'a') as f:
        f.write(f'model:{model}' + '\n')
        f.write(f'FILE : {filename}\n')
        f.write(f'SCHEMA:{",".join(columns)}')
        f.write(f'\nQ:{question}' + '\n')
        f.write(f'A:{result}' + '\n')
        f.write(f'Correct : {correct}' + '\n\n\n')
        f.close()

def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def get_answer(question, data, settings):
    for key in data.keys():
        if data[key] in ['float64' , 'int64', 'float32' , 'int32']:
            data[key] = "number_TYPE"
        else:
             data[key] = "text_TYPE"

    db_schema = [x.replace(' ', '_').upper()  + " : " + data[x] for x in data.keys()]
 

    url = "http://localhost:8001/gpt"

    data = {
        "db_schema" : db_schema,
        "question" : question,
        "settings" : settings,
    }

    response = requests.post(url, json = data)
    
    return response.json()["data"][0]["sql"]
