import streamlit as st
from langchain_helper import get_few_shot_db_chain
import pandas as pd

st.title("Ecommerce: Database Q&A ")

question = st.text_input("Ask me something about the sales, customers, orders, or products: ")

if question:
    chain = get_few_shot_db_chain()
    with st.spinner("Thinking..."):
        response = chain.run(question)

    st.header("Answer")
    # If the response is a DataFrame, show table and chart
    if isinstance(response, pd.DataFrame):
        st.dataframe(response)
        numeric_cols = response.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            st.bar_chart(response[numeric_cols])
    else:
        st.write(response)
