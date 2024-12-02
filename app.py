import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import tempfile
import PyPDF2

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process audio data from microphone
def process_audio_from_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition service error: {e}")
        return ""

# Streamlit App
st.title("Job Application Assistant")

# Step 1: Input Section
st.header("Step 1: Provide Inputs")

# Resume upload
resume_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

# Job Description input
job_description = st.text_area("Enter Job Description (Text)", height=150)

# Job Profile input
job_profile = st.text_input("Enter Job Profile (Text)")

# Step 2: Display Extracted Text
if st.button("Submit Inputs"):
    if resume_file and job_description and job_profile:
        # Parse the resume PDF
        extracted_resume_text = extract_text_from_pdf(resume_file)
        
        # Display parsed text (optional)
        st.subheader("Parsed Resume Content:")
        st.text(extracted_resume_text)

        st.success("Inputs submitted successfully! Proceed to Chatbot interface.")
        st.session_state["chat_ready"] = True
        st.session_state["resume_text"] = extracted_resume_text
        st.session_state["job_description"] = job_description
        st.session_state["job_profile"] = job_profile
    else:
        st.error("Please provide all inputs.")

# Step 3: Chatbot Interface
if "chat_ready" in st.session_state and st.session_state["chat_ready"]:
    st.header("Chatbot Interface")
    user_input = st.text_input("Type your message here:")

    # Microphone Input
    st.subheader("Record via Microphone")
    webrtc_ctx = webrtc_streamer(key="speech-rec", mode=WebRtcMode.SENDRECV)

    if webrtc_ctx.audio_receiver:
        audio_frames = webrtc_ctx.audio_receiver.get_frames()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            for frame in audio_frames:
                temp_audio.write(frame.to_ndarray())
            temp_audio_path = temp_audio.name

        if st.button("Process Mic Input"):
            text_output = process_audio_from_file(temp_audio_path)
            if text_output:
                st.success(f"Recognized Speech: {text_output}")

    if user_input:
        st.write(f"You said: {user_input}")
