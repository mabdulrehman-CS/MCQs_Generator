# MCQ Generator 🤖

An end-to-end AI-powered Multiple Choice Questions (MCQ) Generator application built with LangChain, Groq AI, and Streamlit. Upload any PDF or text file and generate customized MCQs instantly!

## 🌐 Live Demo

**Deployed on AWS:** [http://16.171.253.148:8501/](http://16.171.253.148:8501/)

## ✨ Features

- 📄 **File Upload**: Support for PDF and TXT files
- 🧠 **AI-Powered**: Uses Groq AI with Llama 3.3-70B model for intelligent question generation
- 🎯 **Customizable**: Set the number of MCQs (5-50), subject, and difficulty level
- 📊 **Formatted Output**: Questions displayed in a clean table format
- 📝 **Expert Review**: AI evaluates the complexity and quality of generated questions
- 🚀 **Fast Generation**: Powered by Groq's fast inference
- 🎨 **Beautiful UI**: Modern animated interface with gradient backgrounds and smooth transitions
- 💾 **PDF Export**: Download generated MCQs as professionally formatted PDF documents
- ✨ **Animations**: Engaging fade-in, slide-in, and bounce effects throughout the app
- 🎭 **Interactive Design**: Hover effects, glass-morphism, and responsive layouts

## 🛠️ Tech Stack

- **Frontend**: Streamlit with Custom CSS Animations
- **Backend**: Python, LangChain
- **AI Model**: Groq AI (Llama 3.3-70B-Versatile)
- **PDF Generation**: ReportLab
- **Deployment**: AWS EC2 (Ubuntu)

## 📁 Project Structure

```
MCQs_Generator/
├── StreamlitAPP.py          # Main Streamlit application
├── setup.py                 # Package setup configuration
├── requirements.txt         # Python dependencies
├── Response.json            # JSON template for MCQ format
├── data.txt                 # Sample data file
├── test.py                  # Test script
├── .env                     # Environment variables (not in repo)
├── .gitignore               # Git ignore file
├── src/
│   ├── __init__.py
│   └── mcqgenerator/
│       ├── __init__.py
│       ├── mcqgenerator.py  # Core MCQ generation logic with LangChain
│       ├── utils.py         # Utility functions (file reading, data parsing)
│       └── logger.py        # Logging configuration
├── experiment/
│   └── mcqgen.ipynb         # Jupyter notebook for experimentation
└── logs/                    # Application logs
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Groq API Key (Get it from [Groq Console](https://console.groq.com/))

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mabdulrehman-CS/MCQs_Generator.git
   cd MCQs_Generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run StreamlitAPP.py
   ```

6. **Open in browser**
   
   Navigate to `http://localhost:8501`

## ☁️ AWS Deployment Guide

### Step 1: Launch EC2 Instance

1. Launch an Ubuntu EC2 instance (t2.micro or higher)
2. Configure Security Group to allow:
   - SSH (Port 22)
   - Custom TCP (Port 8501)

### Step 2: Connect to EC2

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Setup Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/mabdulrehman-CS/MCQs_Generator.git
cd MCQs_Generator

# Install dependencies
pip3 install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### Step 5: Run Application

```bash
# Run Streamlit (basic)
python3 -m streamlit run StreamlitAPP.py --server.port 8501 --server.address 0.0.0.0

# Run in background (recommended for production)
nohup python3 -m streamlit run StreamlitAPP.py --server.port 8501 --server.address 0.0.0.0 &
```

### Step 6: Access Application

Open `http://your-ec2-public-ip:8501` in your browser.

## 📖 How to Use

1. **Upload a File**: Click "Browse files" and upload a PDF or TXT file containing the content you want to generate MCQs from.

2. **Set Parameters**:
   - **Number of MCQs**: Choose between 5-50 questions
   - **Subject**: Enter the subject (e.g., "Machine Learning", "Biology")
   - **Complexity Level**: Enter difficulty (e.g., "Easy", "Medium", "Hard")

3. **Generate**: Click "✨ Generate MCQs" button and watch the beautiful animations!

4. **View Results**: The generated MCQs will be displayed in an interactive table format with an expert review analysis.

5. **Download PDF**: Click the "📄 Download MCQs as PDF" button to save your questions as a professionally formatted PDF document with:
   - Subject header and metadata
   - All questions with choices
   - Correct answers highlighted
   - Complete AI review and analysis
   - Automatic filename with subject and timestamp

## 🎨 UI Features

The application now features a modern, animated interface with:

- **Animated Gradient Background**: Smooth color transitions between purple, pink, and blue
- **Fade-in Animations**: Title and form elements animate smoothly on page load
- **Glass-morphism Design**: Semi-transparent form with blur effect
- **Interactive Elements**: Hover effects on buttons, inputs, and table rows
- **Success Feedback**: Balloons and animated success messages
- **Professional Typography**: Google Poppins font throughout
- **Responsive Layout**: Two-column form design for better organization
- **Styled Components**: Rounded corners, shadows, and smooth transitions
- **Color-coded UI**: Purple/pink gradient theme for visual consistency

## 🔧 Configuration

### Groq Model

The application uses `llama-3.3-70b-versatile` model. You can change this in `src/mcqgenerator/mcqgenerator.py`:

```python
llm = ChatGroq(
    groq_api_key = key,
    model_name="llama-3.3-70b-versatile"  # Change model here
)
```

### Available Groq Models
- `llama-3.3-70b-versatile`
- `llama3-70b-8192`
- `llama3-8b-8192`
- `mixtral-8x7b-32768`

### Core Functions

- `read_file(file)`: Reads and extracts text from PDF or TXT files
- `get_table_data(quiz)`: Parses quiz JSON and formats it for display
- `generate_evaluate_chain`: LangChain chain that generates and evaluates MCQs
- `create_pdf(df, review, subject, mcq_count, tone)`: Generates professionally formatted PDF documents with all MCQ data

## 📦 Dependencies

Key Python packages used:

```
langchain              # LLM framework
langchain-core         # Core LangChain components
langchain-groq         # Groq AI integration
groq                   # Groq API client
streamlit              # Web interface
python-dotenv          # Environment variables
PyPDF2                 # PDF file reading
pandas                 # Data manipulation
reportlab              # PDF generation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Muhammad Abdul Rehman**
- GitHub: [@mabdulrehman-CS](https://github.com/mabdulrehman-CS)

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing LLM framework
- [Groq](https://groq.com/) for fast AI inference
- [Streamlit](https://streamlit.io/) for the easy-to-use web framework

---

⭐ If you found this project helpful, please give it a star!