from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2
import google.generativeai as genai
from google.generativeai.models import get_model

load_dotenv()
API = os.getenv("GOOGLE_GEMINI_API")

genai.configure(api_key=API)

# model = genai.model('gemini-pro-vision')
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(prompt,pdf,input_text):
    response = model.generate_content([input_text,pdf[0],prompt])
    return response.text
def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
            return pdf_text
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return None  # Indicate error
    else:
        st.error("Please upload a PDF resume.")
        return None

# streamlit shabang

st.set_page_config(page_title="Resume Analyzer")

st.header("HR x Gemini")
input_text = st.text_input("Enter keywords/criteria to analyze (e.g., skills, experience):")
upload_info = st.info("Upload your resume in PDF format.")
uploaded_file = st.file_uploader("Select Resume PDF", type=["pdf"])

# if uploaded_file:
#     resume = Image.open(uploaded_file)
#     st.image(resume, caption="Uploaded Resume", use_column_width=True)


submit = st.button("Submit")

input_prompt = "You are an expert understanding Resume of the people to decide  if they can be hired or not. you are able to understand given keywords are there in the resume or not and if not all then how many are there based on that you take a decision to hire or not."

# if submit button clicked
if submit:
    pdf_data = extract_pdf_text(uploaded_file)
    response = get_gemini_response(input_prompt,pdf_data,input_text)
    st.write(response)