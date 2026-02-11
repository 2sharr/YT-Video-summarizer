diff --git a/README.md b/README.md
index 01091af2a22c38d4319ce1378781191b769c229c..66b18f52e5a224e2c0711cc888406496d19dd3c8 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,285 @@
 # YT-Video-summarizer
+
+A lightweight Python project that:
+1. Reads a YouTube video transcript,
+2. Uses Google Gemini to summarize it,
+3. Exports a styled `index.html` summary page.
+
+---
+
+## 1) Project overview and purpose
+
+`YT-Video-summarizer` is a script-first utility for quickly generating concise summaries of YouTube videos from their transcripts. It is ideal for:
+- fast content triage,
+- study/review workflows,
+- creating shareable summary snippets in HTML format.
+
+The current implementation is intentionally simple and centered around one script (`app.py`) with a fixed input video URL constant (`YOUTUBE_LINK`).
+
+---
+
+## 2) Getting started (installation, dependencies, setup)
+
+### Prerequisites
+- Python 3.9+
+- A Google AI API key with access to Gemini models
+- Internet access (for YouTube transcript retrieval and Gemini API calls)
+
+### Clone the repository
+```bash
+git clone <your-repo-url>
+cd YT-Video-summarizer
+```
+
+### Create and activate a virtual environment
+
+**macOS/Linux**
+```bash
+python3 -m venv .venv
+source .venv/bin/activate
+```
+
+**Windows (PowerShell)**
+```powershell
+python -m venv .venv
+.venv\Scripts\Activate.ps1
+```
+
+### Install dependencies
+```bash
+pip install -r requirements.txt
+```
+
+Current dependencies include transcript extraction, Gemini client, dotenv loading, and Streamlit (installed but not used in the current script).
+
+### Environment setup
+Create a `.env` file in the project root:
+
+```dotenv
+GOOGLE_API_KEY=your_google_api_key_here
+```
+
+The application loads environment variables via `python-dotenv` and configures `google-generativeai` using `GOOGLE_API_KEY`.
+
+---
+
+## 3) Build, test, and run commands (with examples)
+
+> This repository is a Python script project (no separate compile/build artifact).
+
+### Run
+```bash
+python app.py
+```
+
+### Basic code sanity check
+```bash
+python -m py_compile app.py
+```
+
+### Optional dependency snapshot
+```bash
+pip freeze > requirements.lock.txt
+```
+
+---
+
+## 4) Usage and examples (CLI/UX as applicable)
+
+### Current usage flow
+1. Open `app.py`.
+2. Set `YOUTUBE_LINK` to the desired video URL.
+3. Run `python app.py`.
+4. Open generated `index.html` in your browser.
+
+The script extracts transcript text, summarizes it with Gemini, and writes styled HTML output to `index.html`.
+
+### Example
+```python
+# in app.py
+YOUTUBE_LINK = "https://www.youtube.com/watch?v=VIDEO_ID"
+```
+
+Then:
+```bash
+python app.py
+```
+
+Expected console output:
+```text
+✅ index.html saved.
+```
+
+---
+
+## 5) Architecture and key components
+
+### High-level flow
+
+```text
+YouTube URL
+   │
+   ▼
+extract_transcript_details()
+   │   (youtube_transcript_api)
+   ▼
+transcript string
+   │
+   ▼
+generate_summary()
+   │   (google-generativeai / Gemini)
+   ▼
+summary text
+   │
+   ▼
+save_to_html()
+   │
+   ▼
+index.html
+```
+
+### Key modules/functions
+- `extract_transcript_details(youtube_video_url)`
+  - Parses video ID from URL and fetches transcript data from YouTube transcript API.
+- `generate_summary(transcript)`
+  - Builds a prompt and calls Gemini (`gemini-pro`) to generate a concise summary.
+- `save_to_html(summary)`
+  - Converts summary newlines to `<br>` and writes a simple styled HTML file.
+
+Entry point execution order is defined under `if __name__ == "__main__":`.
+
+---
+
+## 6) Configuration options, environment variables, and secrets handling
+
+### Configuration options
+- `YOUTUBE_LINK` (hard-coded constant in `app.py`) controls the target video URL.
+- Prompt text and word limit are currently hard-coded in `generate_summary()`.
+
+### Environment variables
+- `GOOGLE_API_KEY` (**required**): used to authenticate Gemini API usage.
+
+### Secrets handling best practices
+- Store secrets in `.env` locally; never commit `.env` to source control.
+- Rotate keys if exposed.
+- In CI/CD or deployment platforms, inject `GOOGLE_API_KEY` through secure secret managers.
+
+---
+
+## 7) Deployment instructions (staging/production)
+
+### Current status
+Not applicable as a production web service in its current form. This is a local/batch script that outputs static HTML.
+
+### Suggested deployment paths
+- **Containerized batch job** (e.g., cron-triggered run with mounted output directory)
+- **Serverless function** wrapping transcript+summary logic (with explicit URL input)
+- **Streamlit app** (dependency already present) for interactive UX
+
+For staging/production hardening, add:
+- argument parsing (`--url`),
+- structured logging,
+- retries/timeouts,
+- error classification,
+- monitoring/alerts.
+
+---
+
+## 8) Testing strategy and commands
+
+### Current strategy
+The project currently has no dedicated unit/integration test suite.
+
+### Recommended baseline
+- Unit tests for:
+  - URL parsing and video ID extraction
+  - HTML output generation
+  - API error handling paths
+- Integration test (mocked external APIs where possible)
+
+### Commands
+```bash
+# syntax/bytecode check
+python -m py_compile app.py
+
+# (future) once tests are added
+pytest -q
+```
+
+---
+
+## 9) Contribution guidelines (branching, PR process)
+
+### Branching model (recommended)
+- `main`: stable/default branch
+- `feature/<short-description>` for new work
+- `fix/<short-description>` for bug fixes
+
+### Contribution workflow
+1. Fork/clone repository.
+2. Create feature branch.
+3. Make focused changes.
+4. Run local checks (`python -m py_compile app.py`).
+5. Open PR with:
+   - problem statement,
+   - change summary,
+   - validation steps,
+   - screenshots/output samples when UX changes.
+
+### Commit style (recommended)
+Use clear conventional-style messages, e.g.:
+- `docs: expand README with setup, architecture, and deployment guidance`
+- `feat: add CLI input for youtube url`
+
+---
+
+## 10) Known issues, limitations, and to-do list
+
+### Known limitations
+- Input URL is hard-coded in source instead of CLI/API input.
+- Basic URL parsing assumes `v=` query format and may fail for shortened URLs (`youtu.be/...`).
+- Error handling returns error strings that are passed forward as content (no typed exceptions or early exits).
+- Uses model name `gemini-pro`; availability may vary by API version/account.
+- No automated tests yet.
+
+### To-do
+- Add argparse-based CLI (`--url`, `--output`, `--max-words`).
+- Add robust URL parsing utilities.
+- Add retry/backoff strategy for transient API failures.
+- Add tests with mocks.
+- Add Streamlit interface or REST API wrapper.
+
+---
+
+## 11) Licensing and author information
+
+### License
+No license file is currently present in this repository.
+
+> Recommended: add `LICENSE` (e.g., MIT, Apache-2.0, or proprietary as appropriate).
+
+### Author / maintainers
+Not explicitly specified in repository metadata. Add maintainers/contact section when available.
+
+---
+
+## 12) Project-specific conventions or notes
+
+- The script currently writes output to `index.html` in repository root by default.
+- The generated HTML uses inline dark theme styling for quick local viewing.
+- `streamlit` is listed in dependencies but no Streamlit app entrypoint exists yet.
+
+---
+
+## Quick start (TL;DR)
+
+```bash
+python3 -m venv .venv
+source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
+pip install -r requirements.txt
+
+# create .env with GOOGLE_API_KEY
+python app.py
+```
+
+Open `index.html` to view your summary.
