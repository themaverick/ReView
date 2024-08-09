# Import the Python SDK
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd
from prompts import prompt1, prompt2
from pyhtml2pdf import converter

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI-API-KEY")

def set_connection(key = GEMINI_API_KEY, model_name = "gemini-1.5-flash"):
    genai.configure(api_key=key)

    model = genai.GenerativeModel(model_name)
    return model

def getStructRevws(dataframe):

    reviews = dataframe
    reviews = reviews.drop(reviews.columns[0], axis = 1)
    reviews.rename(columns = {'content': 'body'}, inplace = True)
    rvwStruct = {"reviews": []}

    for i in range(len(reviews['title'])):
        inst = reviews.iloc[i]
        rvw = {"rating": inst['rating'], "title": inst['title'], "body": inst['body']}
        rvwStruct['reviews'].append(rvw)

    return rvwStruct

def getHTMLreport(model, rvwStruct):
    promptRvw = prompt1.format(structuredReviews = rvwStruct)
    rvwReport = model.generate_content(promptRvw)

    promptStructRvw = prompt2.format(report = rvwReport.text)
    structuredReport = model.generate_content(promptStructRvw)

    with open("index.html", "w",encoding="utf-8") as file:
        file.write(structuredReport.text)

    print("index.html has been created!")

    path = os.path.abspath('index.html')
    converter.convert(f'{path}', 'sample.pdf')

    print(f"PDF saved.")

def inference(dataframe):
    print("\n Got dataframe \n establishing connection with llm \n")
    model = set_connection()
    print("\n connected to LLM\nStructuring reviews \n")
    structured_reviews = getStructRevws(dataframe)
    print("\n Got structured reviews.\nGenerating report \n")
    getHTMLreport(model = model, rvwStruct=structured_reviews)
    print("\nReport Generated\n")

    
