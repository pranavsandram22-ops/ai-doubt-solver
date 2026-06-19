iimport streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Optional microphone support
try:
    from audio_recorder_streamlit import audio_recorder
    mic_available = True
except:
    mic_available = False

# API Keys
API_KEYS = [
    st.secrets["GEMINI_API_KEY1"],
    st.secrets["GEMINI_API_KEY2"],
    st.secrets["GEMINI_API_KEY3"]
]

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


def ask_gemini(prompt, image=None):

    for key in API_KEYS:

        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            if image is not None:
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)

            return response.text

        except:
            continue

    return "⚠️ All API keys are busy. Please try again later."


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

                    answer = ask_gemini(
                        f"""
Explain this image clearly.
Use simple words and examples.

Question:
{question}
""",
                        image
                    )

                else:

                    answer = ask_gemini(
                        f"""
Explain the following doubt in simple words with examples.

Question:
{question}
"""
                    )

            st.subheader("✅ Answer")
            st.write(answer)