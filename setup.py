from setuptools import setup, find_packages


setup(    
    name='mcqgenerator',
    version='0.0.1',
    author='abdul rehman',
    author_email="mabdulrehman.cui@gmail.com",
    install_requires=[
        "langchain-groq",
        "langchain-core",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "pandas",
    ],
    packages=find_packages()
)