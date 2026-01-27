import os
import sys
import json
import pandas as pd
import streamlit as st
import traceback
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcqgenerator.utils import read_file, get_table_data
from mcqgenerator.mcqgenerator import generate_evaluate_chain, RESPONSE_JSON
from mcqgenerator.logger import logging

# Load environment variables
load_dotenv()

#Creating a title for the app
st.title("MCQ Generator and Evaluator with LangChain and GroqAI 🤖")

with st.form("user input"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    mcq_count = st.number_input("Number of MCQs", min_value=5, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=50)
    tone = st.text_input("Complexity Level of MCQs (e.g., Easy, Medium, Hard)", max_chars=20, placeholder="e.g., Easy, Medium, Hard")

    button = st.form_submit_button("Generate MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Generating MCQs..."):
        try:
            # Read and extract text from the uploaded file
            text = read_file(uploaded_file)

            # Generate MCQs using the chain (Groq doesn't have token callbacks like OpenAI)
            response = generate_evaluate_chain.invoke(
                {
                "text": text,
                "number": mcq_count,
                "subject": subject,
                "tone": tone,
                "RESPONSE_JSON": json.dumps(RESPONSE_JSON)}
            )

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error(f"Error: {e}")

        else:
            if isinstance(response, dict):
                #Extract the quiz from the response dictionary
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1  # Start index from 1
                        st.table(df)

                        #display the review in a text box as well
                        st.text_area(label="Review", value=response.get("review", ""))
                    else:
                        st.error("Error in the table data.")
                else:
                    st.error("No quiz generated.")
            else:
                st.write(response)