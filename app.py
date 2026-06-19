import streamlit as st
import requests
from PIL import Image
import time

# Optional microphone support
try:
    from audio_recorder_streamlit import audio_recorder
    mic_available = True
except:
    mic_available = False

# OpenRouter API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Logo
st.image("logo.png", width=150)

# Title
st.title("🤖 AI Doubt Solver")
st.write("Ask doubts using text, voice, or images.")

# Cooldown
if "last_request" not in st.session_state:
    st.session_state.last_request = 0

# Text input
question = st.text_input("❓ Enter your doubt")

# Microphone
st.subheader("🎤 Voice Input")

if mic_available:
    audio_bytes = audio_recorder(
        text="Click to record",
        recording_color="#e74c3c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="2x"
    )

    if audio_bytes:
        st.success("Voice recorded!")
        st.audio(audio_bytes, format="audio/wav")

else:
    st.warning("Microphone unavailable.")

# Image upload
uploaded_file = st.file_uploader(
    "📷 Upload an image (optional)",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    MODELS = [
        "meta-llama/llama-3.3-8b-instruct:free",
        "google/gemma-3-12b-it:free",
        "mistralai/mistral-7b-instruct:free"
    ]

    for model_name in MODELS:

        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()

            st.write("Model:", model_name)
            st.write(result)

            if "choices" in result:
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            st.error(e)

    return "All models failed."


# Button
if st.button("🚀 Explain"):

    current_time = time.time()

    if current_time - st.session_state.last_request < 10:
        st.warning("⏳ Please wait 10 seconds before asking another doubt.")

    else:

        st.session_state.last_request = current_time

        if question.strip() == "" and image is None:
            st.warning("Please enter a question or upload an image.")

        else:

            with st.spinner("Thinking..."):

                if image is not None:

                    answer = ask_ai(
                        f"""
Explain this image clearly.
Use simple words and examples.

Question:
{question}
"""
                    )

                else:

                    answer = ask_ai(
                        f"""
Explain the following doubt in simple words with examples.

Question:
{question}
"""
                    )

            st.subheader("✅ Answer")
            st.write(answer)