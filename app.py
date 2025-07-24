import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ CHANGE THIS LINK
YOUTUBE_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # ← replace this with your video

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        return f"Transcript fetch error: {str(e)}"

def generate_summary(transcript):
    try:
        prompt = (
            "You are a YouTube video summarizer. Please summarize the following transcript "
            "in clear points under 250 words:\n\n"
        )
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript)
        return response.text
    except Exception as e:
        return f"Summary generation error: {str(e)}"

def save_to_html(summary):
    summary = summary.replace("\n", "<br>")
    html = f"""
    <html>
      <head><title>YouTube Summary</title></head>
      <body style="background-color:#111;color:white;font-family:sans-serif;padding:2rem;">
        <h1>YouTube Video Summary</h1>
        <p>{summary}</p>
      </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html saved.")

if __name__ == "__main__":
    transcript = extract_transcript_details(YOUTUBE_LINK)
    summary = generate_summary(transcript)
    save_to_html(summary)
