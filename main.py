import json
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            sub_category, mandatory_fields = process_product(product_name)
            return render_template('results.html', sub_category=sub_category, mandatory_fields=mandatory_fields)
    return render_template('index.html')


def process_product(product_name):
    answer = agent.invoke(f"What sub-category does {product_name} belong to, and if it does not exist, find the sub-category that is similar to it? Return the most related sub-category as output, then get the columns that have value 'M' for that sub-category and return them as a dictionary.")
    text = answer["output"]
    start_index = text.find("{")
    json_data = text[start_index:]
    json_data = json.loads(json_data)
    mandatory_fields = [key for key, value in json_data.items() if value == 'M']
    sub_category = json_data.get('sub_category', 'Formal Shoes')
    return sub_category, mandatory_fields


if __name__ == '__main__':
    app.run()
