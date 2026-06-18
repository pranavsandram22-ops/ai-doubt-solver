import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# App Title
st.title("🤖 AI Doubt Solver")

# Text Input
question = st.text_input("Enter your doubt or ask about an image:")

# Image Upload
uploaded_file = st.file_uploader(
    "Upload an image (optional)",
    type=["jpg", "jpeg", "png"]
)

# Display uploaded image
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Button
if st.button("Explain"):

    # If image uploaded
    if image is not None:
        response = model.generate_content(
            [question, image]
        )

    # Text-only question
    else:
        response = model.generate_content(
            f"Explain this topic in simple words with examples: {question}"
        )

    st.write("### Answer:")
    st.write(response.text)