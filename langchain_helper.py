import os
import google.generativeai as genai
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

DB_URL = "mysql+pymysql://root:root@localhost/ecommerce"

def get_few_shot_db_chain():
    class Chain:
        def run(self, question):
            prompt = f"""You are a helpful assistant. Convert the following natural language question into a syntactically correct MySQL query. 
Only generate the SQL query, nothing else.

Question: {question}
SQL:"""
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)
            sql_query = response.text.strip().split('\n')[0]

            engine = create_engine(DB_URL)
            try:
                with engine.connect() as conn:
                    result = pd.read_sql(sql_query, conn)
                return result
            except Exception as e:
                return f"Error running SQL: {e}\nGenerated SQL: {sql_query}"

    return Chain()

import sys
print("Python executable:", sys.executable)
print("google.generativeai location:", genai.__file__)
