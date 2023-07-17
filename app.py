import streamlit as st
import openai
import pandas as pd
import os
from typing import TextIO
from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI


st.set_page_config(page_title="Ask Your CSV? 📈")
st.header("Ask Your CSV? 📈 ")
uploaded_file = st.file_uploader("Upload your csv file", type="csv")

def get_answer_csv(uploaded_file: st.file_uploader, query: str) -> str:
    df = pd.read_csv(uploaded_file)
    path = df.to_string()

    file_path = os.path.abspath(path)

    if os.path.exists(file_path):
        agent = create_csv_agent(OpenAI(temperature=0), file_path, verbose=False)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

    answer = agent.run(query)
    return answer

if uploaded_file is not None:
    query = st.text_area("Ask a question about your CSV file: ")
    button = st.button("Submit")
    if button:
        st.write(get_answer_csv(str(uploaded_file), query))


os.environ["OPENAI_API_KEY"] = ""
