import streamlit as st
import google.generativeai as genai
from PIL import Image
from audio_recorder_streamlit import audio_recorder

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Lightweight model
model = genai.GenerativeModel("gemini-1.5-flash")

# Logo
st.image("logo.png", width=150)

# Title
st.title("🤖 AI Doubt Solver")
st.write("Ask any doubt using text, voice, or images.")

# Text input
question = st.text_input("❓ Enter your doubt")

# Voice input
st.subheader("🎤 Voice Input")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e74c3c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x",
)

if audio_bytes:
    st.success("✅ Voice recorded successfully!")
    st.audio(audio_bytes, format="audio/wav")
    st.info(
        "Voice recording is available. Speech-to-text conversion can be added later."
    )

# Image upload
uploaded_file = st.file_uploader(
    "📷 Upload an image (optional)",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Button
if st.button("🚀 Explain"):

    if question.strip() == "" and image is None:
        st.warning("Please enter a question or upload an image.")

    else:

        try:

            if image is not None:

                response = model.generate_content(
                    [
                        f"""
Explain this image clearly.
Give step-by-step explanation.
Use simple words and examples.

User Question:
{question}
                        """,
                        image
                    ]
                )

            else:

                response = model.generate_content(
                    f"""
Explain the following doubt in simple words with examples.

Question:
{question}
                    """
                )

            st.subheader("✅ Answer")
            st.write(response.text)

        except Exception:

            st.error(
                "⚠️ Too many requests or API limit reached.\n\nPlease wait a minute and try again."
            )