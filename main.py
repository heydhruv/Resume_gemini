from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()
API = os.getenv("GOOGLE_GEMINI_API")

genai.configure(API=API)

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_text,image,prompt):
    response = model.generate_content([input_text,image[0],prompt])
    return response.text


# streamlit shabang


