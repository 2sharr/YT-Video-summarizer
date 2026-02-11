# YT-Video-Summarizer

A Python utility that: 1. Extracts YouTube transcripts 2. Uses Google
Gemini to summarize 3. Exports styled HTML output

------------------------------------------------------------------------

## Requirements

-   Python 3.9+
-   Google API Key
-   Internet connection

------------------------------------------------------------------------

## Setup

``` bash
git clone <your-repo-url>
cd YT-Video-summarizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create .env file:

    GOOGLE_API_KEY=your_google_api_key

------------------------------------------------------------------------

## Run

``` bash
python app.py
```

Open `index.html` to view the summary.

------------------------------------------------------------------------

## Architecture

YouTube URL → Transcript Extraction → Gemini Summary → HTML Output

------------------------------------------------------------------------

## Known Limitations

-   Hardcoded YouTube URL
-   Basic error handling
-   No automated tests

------------------------------------------------------------------------

## Future Enhancements

-   Add CLI input
-   Improve URL parsing
-   Add retry handling
-   Add unit tests
