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

# Define the summarization prompt
default_prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        print(f"Transcript fetch error: {str(e)}")
        return None

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        print(f"Summary generation error: {str(e)}")
        return None

def summarize_and_save(youtube_link, language="English"):
    transcript_text = extract_transcript_details(youtube_link)
    if not transcript_text:
        return

    if language == "Hindi":
        prompt = "Please summarize the following video transcript in Hindi:\n"
    elif language == "Marathi":
        prompt = "Please summarize the following video transcript in Marathi:\n"
    else:
        prompt = default_prompt

    summary = generate_gemini_content(transcript_text, prompt)
    if summary:
        # Replace newlines with <br> separately to avoid f-string escape issues
        summary_html = summary.replace("\n", "<br>")

        html_content = """
        <html>
            <head><title>YT Summary</title></head>
            <body style="font-family:sans-serif; padding:2rem; background:#111; color:white;">
                <h1>Video Summary</h1>
                <p>{}</p>
            </body>
        </html>
        """.format(summary_html)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("Summary saved to index.html")
    else:
        print("Failed to generate summary.")

# ---------- Entry Point ----------
if __name__ == "__main__":
    # Non-interactive mode for GitHub Actions
    if os.getenv("CI", "false").lower() == "true":
        default_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with real or dummy link
        summarize_and_save(default_link, language="English")
    else:
        # Streamlit UI
        st.set_page_config(page_title="YouTube Video Summarizer", page_icon="📺", layout="wide")
        st.title("YouTube Video Summarizer 🎥")
        youtube_link = st.text_input("Enter YouTube Video Link:")
        language = st.selectbox("Select Language for Summary:", ["English", "Hindi", "Marathi"], index=0)

        if youtube_link:
            try:
                video_id = youtube_link.split("v=")[1].split("&")[0]
                thumbnail = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                st.image(thumbnail, use_container_width=True)
            except:
                st.warning("Invalid YouTube URL")

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                time.sleep(2)
                summarize_and_save(youtube_link, language)

                if os.path.exists("index.html"):
                    with open("index.html", "r", encoding="utf-8") as f:
                        st.markdown("## Summary:")
                        st.components.v1.html(f.read(), height=500, scrolling=True)
                else:
                    st.error("Failed to generate summary.")
