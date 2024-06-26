import re
import streamlit as st
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

import pandas as pd
import json

df = pd.read_json("Taxonomy-Fashion.json")
import os

os.environ["OPENAI_API_KEY"] = st.secrets["openai_secret_key"]
agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

def extract_quotes(text):
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, text)
    return matches

def process_product(product_name):
    
    answer = agent.invoke(f"What sub-category does {product_name} belongs to , if it does not exist find the sub-category that is similar to it? and return the most related sub-category as output then get the columns that has value M for that sub-category and return the them as a dictionary instead of a string.")
    text = answer["output"]
    lis = extract_quotes(text) 
    if product_name.lower() == lis[0].lower():        
        sub_category = lis[1]
    else:
        sub_category = lis[0]     
    start_index = text.find("{")
    json_data = text[start_index:]

    json_data = json.loads(json_data)
    field = list(json_data.keys())
    mandatory_fields = field
    return sub_category, mandatory_fields


def main():
    st.set_page_config(page_title="Product Categorizer App")
    st.title("Product Categorizer")    
    
    product_name = st.text_input("Enter Product Name:" , )

    if product_name:
        with st.spinner('Processing...'):
            sub_category, mandatory_fields = process_product(product_name)

        col1, col2, col3 = st.columns(3)
        with col2:
            st.subheader("Sub-Category")
        
        
        st.info(sub_category)
        col1, col2, col3 = st.columns(3)
        with col2:
            st.subheader("Mandatory Fields")
        for field in mandatory_fields:
            st.info(field)

if __name__ == "__main__":
    main()

