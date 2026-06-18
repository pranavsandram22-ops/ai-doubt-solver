import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🤖 AI Doubt Solver")

question = st.text_input("Enter your doubt:")

if st.button("Explain"):
    response = model.generate_content(
        f"Explain this topic in simple words with an example: {question}"
    )

    st.write(response.text)