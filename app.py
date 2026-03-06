# Import required libraries
import streamlit as st
from google import genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv


# ----------------------------------------------------
# Load environment variables (for API key security)
# ----------------------------------------------------
load_dotenv()

# Configure Gemini API using key stored in .env file

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ----------------------------------------------------
# Function to get response from Gemini model
# ----------------------------------------------------
def get_gemini_response(prompt):
    """
    Sends formatted prompt to Gemini model
    and returns the generated text response.
    """
    response = client.models.generate_content( model = "gemini-3-flash-preview" , contents=prompt)
    return response.text


# ----------------------------------------------------
# Function to extract text from uploaded PDF
# ----------------------------------------------------
def extract_pdf_text(uploaded_file):
    """
    Reads uploaded PDF file and extracts text
    from all pages.
    """
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    # Correct way to iterate through pages
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text

    return text


# ----------------------------------------------------
# Prompt Template
# (We will dynamically inject resume + JD into this)
# ----------------------------------------------------
input_prompt = """
Act like a highly skilled ATS (Application Tracking System) 
with deep understanding of Software Engineering, Data Science, 
Data Analysis, and Big Data roles.

Your task:
1. Evaluate the resume against the job description.
2. Consider the competitive job market.
3. Assign a percentage match.
4. Identify missing keywords.
5. Provide an improved profile summary.

Resume:
{text}

Job Description:
{jd}

Respond ONLY in valid JSON format like this:

{{
  "JD Match": "85%",
  "MissingKeywords": ["Python", "AWS", "Docker"],
  "Profile Summary": "Improved professional summary here"
}}
"""


# ----------------------------------------------------
# Streamlit UI
# ----------------------------------------------------
st.title("Homie ATS")
st.write("One stop solution to get your resume analysed")

# Text area for Job Description
jd = st.text_area("Paste the Job Description")

# File uploader for Resume
uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type="pdf",
    help="Please upload your resume in PDF format"
)

# Submit button
submit = st.button("Submit")


# ----------------------------------------------------
# Button Logic
# ----------------------------------------------------
if submit:
    if uploaded_file is not None and jd.strip() != "":

        # Extract resume text from PDF
        resume_text = extract_pdf_text(uploaded_file)

        # Inject resume text + JD into prompt template
        formatted_prompt = input_prompt.format(
            text=resume_text,
            jd=jd
        )

        # Get response from Gemini
        response = get_gemini_response(formatted_prompt)

        # Display response in Streamlit
        st.subheader("ATS Analysis Result")
        st.write(response)

    else:
        st.warning("Please upload a resume and paste the job description.")