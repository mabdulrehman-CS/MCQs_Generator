import os
import sys
import json
import pandas as pd
import streamlit as st
import traceback
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcqgenerator.utils import read_file, get_table_data
from mcqgenerator.mcqgenerator import generate_evaluate_chain, RESPONSE_JSON
from mcqgenerator.logger import logging

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="MCQ Generator AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        animation: gradientShift 15s ease infinite !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        animation: gradientShift 15s ease infinite !important;
    }
    
    @keyframes gradientShift {
        0% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        25% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        50% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        75% { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    }
    
    .stApp {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-weight: 700;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease-out;
        margin-bottom: 2rem;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
        backdrop-filter: blur(10px);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        width: 100% !important;
        animation: buttonGlow 2s ease-in-out infinite !important;
    }
    
    @keyframes buttonGlow {
        0%, 100% { box-shadow: 0 5px 15px rgba(240, 147, 251, 0.4); }
        50% { box-shadow: 0 5px 25px rgba(245, 87, 108, 0.6); }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(245, 87, 108, 0.5) !important;
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #f093fb;
        box-shadow: 0 0 0 3px rgba(240, 147, 251, 0.2);
    }
    
    .stFileUploader {
        border: 2px dashed #f093fb;
        border-radius: 15px;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.05) 0%, rgba(245, 87, 108, 0.05) 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #f5576c;
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
        transform: scale(1.01);
    }
    
    .stDataFrame {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: #f8f9fa;
    }
    
    .success-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: bounceIn 0.6s ease-out;
        box-shadow: 0 5px 20px rgba(67, 233, 123, 0.3);
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .download-btn {
        margin-top: 1rem;
    }
    
    div[data-testid="stSpinner"] > div {
        border-color: #f093fb;
        border-right-color: transparent;
    }
    
    .stAlert {
        border-radius: 10px;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Table styling */
    table {
        animation: fadeIn 0.8s ease-out;
    }
    
    thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    tbody tr:hover {
        background: linear-gradient(90deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%) !important;
        transform: scale(1.01);
        transition: all 0.2s ease;
    }
    </style>
""", unsafe_allow_html=True)

#Creating a title for the app
st.markdown("<h1>📝 MCQ Generator AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem; margin-top: -1rem; margin-bottom: 2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>Powered by LangChain & GroqAI 🤖</p>", unsafe_allow_html=True)


# Function to create PDF
def create_pdf(df, review, subject, mcq_count, tone):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    # Add title
    title = Paragraph(f"<b>{subject} - Multiple Choice Questions</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Add metadata
    meta_data = f"""
    <b>Generated on:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    <b>Number of Questions:</b> {mcq_count}<br/>
    <b>Difficulty Level:</b> {tone}<br/>
    """
    elements.append(Paragraph(meta_data, normal_style))
    elements.append(Spacer(1, 20))
    
    # Add questions
    for idx, row in df.iterrows():
        # Question number and text
        q_text = f"<b>Question {idx}:</b> {row['MCQ']}"
        elements.append(Paragraph(q_text, heading_style))
        elements.append(Spacer(1, 6))
        
        # Choices
        choices = row['Choices'].replace('||', '<br/>')
        elements.append(Paragraph(choices, normal_style))
        elements.append(Spacer(1, 6))
        
        # Correct Answer
        correct = f"<b>Correct Answer:</b> <font color='green'>{row['Correct']}</font>"
        elements.append(Paragraph(correct, normal_style))
        elements.append(Spacer(1, 20))
    
    # Add page break before review
    elements.append(PageBreak())
    
    # Add review section
    elements.append(Paragraph("<b>AI Review & Analysis</b>", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(review, normal_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

with st.form("user input"):
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("📄 Upload a PDF or TXT file", type=['pdf', 'txt'])
        subject = st.text_input("📚 Subject", max_chars=50, placeholder="e.g., Python Programming")
    
    with col2:
        mcq_count = st.number_input("🔢 Number of MCQs", min_value=5, max_value=50, value=10)
        tone = st.text_input("🎯 Complexity Level", max_chars=20, placeholder="Easy, Medium, or Hard", value="Medium")

    st.markdown("<br>", unsafe_allow_html=True)
    button = st.form_submit_button("✨ Generate MCQs")

# Store generated data in session state
if 'generated_df' not in st.session_state:
    st.session_state.generated_df = None
if 'generated_review' not in st.session_state:
    st.session_state.generated_review = None
if 'generation_params' not in st.session_state:
    st.session_state.generation_params = {}

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("🎨 Generating MCQs with AI magic..."):
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
            st.error(f"❌ Error: {e}")

        else:
            if isinstance(response, dict):
                #Extract the quiz from the response dictionary
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1  # Start index from 1
                        
                        # Store in session state
                        st.session_state.generated_df = df
                        st.session_state.generated_review = response.get("review", "")
                        st.session_state.generation_params = {
                            'subject': subject,
                            'mcq_count': mcq_count,
                            'tone': tone
                        }
                        
                        st.markdown("<div class='success-box'>✅ MCQs Generated Successfully!</div>", unsafe_allow_html=True)
                        st.balloons()
                        
                        # Display the table
                        st.subheader("📋 Generated Questions")
                        st.dataframe(df, use_container_width=True)

                        # Display the review
                        st.subheader("🔍 AI Review & Analysis")
                        st.text_area(label="", value=response.get("review", ""), height=200, label_visibility="collapsed")
                        
                    else:
                        st.error("❌ Error in the table data.")
                else:
                    st.error("❌ No quiz generated.")
            else:
                st.write(response)

# Display download button if MCQs have been generated
if st.session_state.generated_df is not None:
    st.markdown("---")
    st.subheader("📥 Download Your MCQs")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create PDF
        pdf_buffer = create_pdf(
            st.session_state.generated_df,
            st.session_state.generated_review,
            st.session_state.generation_params['subject'],
            st.session_state.generation_params['mcq_count'],
            st.session_state.generation_params['tone']
        )
        
        # Download button
        st.download_button(
            label="📄 Download MCQs as PDF",
            data=pdf_buffer,
            file_name=f"{st.session_state.generation_params['subject']}_MCQs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )