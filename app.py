import streamlit as st
import PyPDF2
import speech_recognition as sr
from st_custom_component import microphone_input

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process recorded audio
def process_audio(audio_data):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_data) as source:
            audio_content = recognizer.record(source)
            return recognizer.recognize_google(audio_content)
    except sr.UnknownValueError:
        st.error("Could not understand the audio. Please try again.")
    except sr.RequestError as e:
        st.error(f"Speech Recognition service error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
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

    # Microphone Integration
    st.subheader("Record via Mic")
    audio_file = microphone_input(label="Speak Now")

    if st.button("Process Mic Input"):
        if audio_file:
            text_output = process_audio(audio_file)
            if text_output:
                st.success(f"Recognized Speech: {text_output}")

    if user_input:
        st.write(f"You said: {user_input}")
