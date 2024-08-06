# Import the Python SDK
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI-API-KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
