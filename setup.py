from setuptools import setup, find_packages



setup(    
    name='mcqgenerator',
    version='0.0.1',
    author='abdul rehman',
    author_email="mabdulrehman.cui@gmail.com",
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)