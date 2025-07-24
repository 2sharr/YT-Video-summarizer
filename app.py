import streamlit as st
from dotenv import load_dotenv
import os
import time
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer", page_icon="youtube.png", layout="wide")

# Define the summarization prompt
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

# Function to extract transcript details from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID from the URL
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Failed to fetch transcript. Error: {str(e)}")
        return None

# Function to generate summary using Google Generative AI
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate summary. Error: {str(e)}")
        return None

# Streamlit UI components
st.title("YouTube Video Summarizer 🎥")

# Input for YouTube Link
youtube_link = st.text_input("Enter YouTube Video Link:", help="Paste the YouTube video link here.")

# Language selection dropdown
language = st.selectbox("Select Language for Summary:", ["English", "Hindi", "Marathi"], index=0)

# Display video thumbnail if URL is valid
if youtube_link:
    try:
        # Check if the YouTube link is valid by looking for "v=" parameter
        if "v=" in youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]
            video_thumbnail = f"http://img.youtube.com/vi/{video_id}/0.jpg"
            st.image(video_thumbnail, use_container_width=True)
        else:
            st.error("Please enter a valid YouTube URL.")
    except IndexError:
        st.error("Invalid YouTube URL. Please ensure the URL is in the correct format.")

# Button to trigger summarization
if st.button("Summarize", help="Click to generate summary"):
    with st.spinner('Fetching summary...'):
        time.sleep(2)  # Simulate loading time
        if youtube_link:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                # Adjust prompt based on the selected language
                if language == "Hindi":
                    prompt = f"Please summarize the following video transcript in Hindi:\n{transcript_text}"
                elif language == "Marathi":
                    prompt = f"Please summarize the following video transcript in Marathi:\n{transcript_text}"
                else:
                    prompt = f"Please summarize the following video transcript in English:\n{transcript_text}"

                # Generate summary
                summary = generate_gemini_content(transcript_text, prompt)
                if summary:
                    st.markdown("## Summary:")
                    # Use dark mode-friendly styling for both light and dark mode
                    st.markdown(
                        f"<div style='padding: 1rem; background-color: #1e1e1e; color: white; border-radius: 10px;'>{summary}</div>",
                        unsafe_allow_html=True
                    )
