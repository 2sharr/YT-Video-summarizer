# YT-Video-summarizer

A lightweight Python utility that:

1. Reads a YouTube video transcript,
2. Uses Google Gemini to summarize it,
3. Exports a styled `index.html` summary page.

---

## 1) Project overview

`YT-Video-summarizer` is a script-first tool for quickly generating concise summaries of YouTube videos from transcripts. It's ideal for:

- fast content triage,
- study / review workflows,
- creating shareable static HTML summary snippets.

The current implementation is centered on one script (`app.py`) and uses a single hard-coded `YOUTUBE_LINK` constant for the input video.

---

## 2) Prerequisites & install

### Requirements
- Python 3.9+
- Google AI API key with access to Gemini models
- Internet access (to fetch transcripts and call Gemini)

### Clone
```bash
git clone <your-repo-url>
cd YT-Video-summarizer
