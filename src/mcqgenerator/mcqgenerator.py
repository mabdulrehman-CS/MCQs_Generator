# from langchain.llms import OpenAI  <-- (Old OpenAI Import)
# from langchain.chat_models import ChatOpenAI <-- (Old OpenAI Import)
from langchain_groq import ChatGroq # <--- (New Groq Import)

# Updated imports for langchain v0.2+
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSequence

# from langchain.callbacks import get_openai_callback <-- (This specific callback is for OpenAI only. You can remove it or comment it out.)

import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key = key, # Ensure this is in your .env file
    model_name="llama-3.3-70b-versatile"  # Updated to currently supported Groq model
)

# Get the directory where this script is located and find Response.json relative to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RESPONSE_JSON_PATH = os.path.join(PROJECT_ROOT, "Response.json")

with open(RESPONSE_JSON_PATH, "r") as f:
    RESPONSE_JSON = json.load(f)

TEMPLATE = """
Text:{text}
You are an expert an MCQ maker. Given the above text, it is your job to create 
a quiz of {number} multiple choice questions for {subject} students in {tone}.
Make sure the questions are not repeated and check all the questions to be confirming.
Make sure to format your response like RESPONSE_JSON below and use it as a guide
Ensure to make {number} MCQs.
### RESPONSE_JSON
{RESPONSE_JSON}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    template=TEMPLATE
    )

# Using modern LCEL (LangChain Expression Language) instead of deprecated LLMChain
quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz
for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at maz 50 words for complexity analysis.
If the quiz is not as per with the cognitive and analytical capabilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student ability.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
    )

review_chain = quiz_evaluation_prompt | llm | StrOutputParser()

# Using LCEL to create a combined chain that passes outputs between chains
# RunnablePassthrough allows passing the original inputs along with new outputs
from langchain_core.runnables import RunnableLambda

def create_review_input(inputs):
    """Prepare inputs for review chain by adding quiz output"""
    return {
        **inputs,
        "quiz": inputs.get("quiz", "")
    }

# Combined chain: first generates quiz, then reviews it
generate_evaluate_chain = (
    RunnablePassthrough.assign(quiz=quiz_chain)
    | RunnableLambda(lambda x: {**x, "quiz": x["quiz"]})
    | RunnablePassthrough.assign(review=review_chain)
)

