import os
from PyPDF2 import PdfReader
import json
import traceback
import re

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
    elif file.name.endswith('.txt'):
        return file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file format. Please upload a PDF or TXT file.")    

def extract_json_from_text(text):
    """Extract JSON from text that might contain markdown or other content."""
    # Try to find JSON between ```json and ``` markers
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # Try to find JSON between ``` markers
    json_match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # Try to find JSON object in the text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return text

def get_table_data(quiz_str):
    try:
        # Handle if quiz_str is already a dict
        if isinstance(quiz_str, dict):
            quiz_dict = quiz_str
        elif isinstance(quiz_str, str):
            # Extract JSON from text
            quiz_str = extract_json_from_text(quiz_str.strip())
            
            # Try to parse JSON
            try:
                quiz_dict = json.loads(quiz_str)
            except json.JSONDecodeError as e:
                # If JSON is incomplete, try to repair it
                # This is a simple repair - close any open braces
                open_braces = quiz_str.count('{') - quiz_str.count('}')
                open_brackets = quiz_str.count('[') - quiz_str.count(']')
                repaired = quiz_str + ('}' * open_braces) + (']' * open_brackets)
                
                try:
                    quiz_dict = json.loads(repaired)
                except:
                    raise Exception(f"Could not parse JSON even after repair. Original error: {e}")
        else:
            raise Exception(f"Unexpected quiz data type: {type(quiz_str)}")
            
        quiz_table_data=[]
        for key,value in quiz_dict.items():
            mcq = value.get("mcq", value.get("question", ""))
            options = value.get("options", {})
            
            # Format options
            if isinstance(options, dict):
                options_str = " || ".join(
                    [f"{option} -> {option_value}" for option, option_value in options.items()]
                )
            else:
                options_str = str(options)
            
            correct = value.get("correct", value.get("answer", ""))
            
            quiz_table_data.append(
                {
                    "MCQ": mcq,
                    "Choices": options_str,
                    "Correct": correct
                }
            )
        return quiz_table_data
    except Exception as e:
        raise Exception(f"Error parsing quiz data: {e}\nQuiz string preview: {str(quiz_str)[:500] if quiz_str else 'None'}\n{traceback.format_exc()}")