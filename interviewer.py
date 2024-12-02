# import streamlit as st
# import PyPDF2
# import whisper
# import tempfile
# import os

# # Initialize Whisper model
# model = whisper.load_model("base")

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# # Function to convert audio to text using Whisper
# def whisper_speech_to_text(audio_file_path):
#     try:
#         result = model.transcribe(audio_file_path)
#         return result["text"]
#     except Exception as e:
#         st.error(f"An error occurred during transcription: {e}")
#         return ""

# # Streamlit App
# st.title("Job Application Assistant")

# # Step 1: Input Section
# st.header("Step 1: Provide Inputs")

# # Resume upload
# resume_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

# # Job Description input
# job_description = st.text_area("Enter Job Description (Text)", height=150)

# # Job Profile input
# job_profile = st.text_input("Enter Job Profile (Text)")

# # Step 2: Display Extracted Text
# if st.button("Submit Inputs"):
#     if resume_file and job_description and job_profile:
#         # Parse the resume PDF
#         extracted_resume_text = extract_text_from_pdf(resume_file)
        
#         # Display parsed text (optional)
#         st.subheader("Parsed Resume Content:")
#         st.text(extracted_resume_text)

#         st.success("Inputs submitted successfully! Proceed to Chatbot interface.")
#         st.session_state["chat_ready"] = True
#         st.session_state["resume_text"] = extracted_resume_text
#         st.session_state["job_description"] = job_description
#         st.session_state["job_profile"] = job_profile
#     else:
#         st.error("Please provide all inputs.")

# # Step 3: Chatbot Interface
# if "chat_ready" in st.session_state and st.session_state["chat_ready"]:
#     st.header("Chatbot Interface")
#     user_input = st.text_input("Type your message here:")

#     # File uploader for audio recording
#     audio_file = st.file_uploader("Upload an audio file (WAV format preferred)", type=["wav", "mp3", "m4a"])
#     if audio_file:
#         with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
#             temp_audio_file.write(audio_file.read())
#             temp_audio_file_path = temp_audio_file.name

#         st.info("Processing the uploaded audio...")
#         transcription = whisper_speech_to_text(temp_audio_file_path)
#         if transcription:
#             st.text_input("Transcription Result:", value=transcription, key="voice_result")

#     if user_input:
#         st.write(f"You said: {user_input}")
#     elif "voice_result" in st.session_state:
#         st.write(f"Voice Input: {st.session_state['voice_result']}")

import streamlit as st
import PyPDF2
import speech_recognition as sr
import tempfile
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording... Speak into the mic!")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("Recording complete. Processing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.error("Recording timed out. Please try again.")
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
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

    if st.button("Record via Mic"):
        voice_input = speech_to_text()
        if voice_input:
            st.session_state["voice_input"] = voice_input
            st.text_input("Voice Input Result:", value=voice_input, key="voice_result")

    if user_input:
        st.write(f"You said: {user_input}")
    elif "voice_input" in st.session_state:
        st.write(f"Voice Input: {st.session_state['voice_input']}")