import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber

import streamlit as st
# Load the environment variables from the .env file
load_dotenv()
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

# Set your API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Function to analyze resume vs job description
def analyze_resume(resume_text, job_description):
    prompt = f"""
    Given the following job description and resume, analyze the match percentage, missing skills, and areas for improvement.

    **Job Description:**  
    {job_description}

    **Candidate's Resume:**  
    {resume_text}

    Provide insights such as:  
    - Skill match percentage  
    - Key missing skills  
    - Suggestions to improve resume alignment with the job  
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("AI Resume Analyzer 🤖📄")

st.subheader("Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

st.subheader("Paste Job Description")
job_description = st.text_area("Enter the job description here...")

if st.button("Analyze Resume"):
    if uploaded_file and job_description:
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            analysis_result = analyze_resume(resume_text, job_description)
            st.subheader("Analysis Result")
            st.write(analysis_result)
        else:
            st.error("Could not extract text from the uploaded PDF. Please try another file.")
    else:
        st.warning("Please upload a resume and provide a job description.")
