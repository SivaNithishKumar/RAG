from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser

import pandas as pd
import json

df = pd.read_json("Taxonomy-Fashion.json")

import os
os.environ["OPENAI_API_KEY"] = "sk-proj-LVoPf8QczuyrdFTwgjAhT3BlbkFJgxXJDnUi2V3DAQsjd1uO"

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

import streamlit as st
import time

def process_product(product_name):
    time.sleep(2)  
    answer = agent.invoke(f"What sub-category does {product_name} belongs to , if it does not exist find the sub-category that is similar to it? and return the most related sub-category as output then get the columns that has value M for that sub-category and return the them as a dictionary instead of a string.")
    text = answer["output"]

    start_index = text.find("{")


    json_data = text[start_index:]

    json_data = json.loads(json_data)
    field = list(json_data.keys())
    sub_category = "Formal Shoes"
    mandatory_fields = field
    return sub_category, mandatory_fields


def main():
    st.title("Product Information")

    product_name = st.text_input("Enter Product Name:")

    if product_name:
        with st.spinner('Processing...'):
            sub_category, mandatory_fields = process_product(product_name)

        st.subheader("Sub-Category")
        st.write(sub_category)

        st.subheader("Mandatory Fields")
        for field in mandatory_fields:
            st.info(field)

if __name__ == "__main__":
    main()

