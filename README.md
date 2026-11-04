# 🎧 AI Music Studio — Lyrics-to-Visual Concept Generator

A beginner-friendly Generative AI project built with Python and Streamlit. It transforms a lyric excerpt into a creative music concept: lyric interpretation, track title, sound direction, colour palette, visual motifs, and an album-art prompt.

## Features
- Lyrics input area
- Mood, genre and artwork-style controls
- Optional live text generation using Google Gemini (`gemini-2.5-flash`)
- Built-in demo mode so the app can still be explored without an API key
- Downloadable JSON creative brief
- Dark, music-studio inspired interface

> The app generates an image prompt, not an actual image. You can paste that prompt into an image generator.

## 1. Open in VS Code
1. Extract the ZIP file.
2. Open the `AI_Music_Studio` folder in VS Code.
3. Open **Terminal → New Terminal**.

## 2. Create and activate a virtual environment

### Windows PowerShell
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\\Scripts\\Activate.ps1
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run the app
```bash
streamlit run app.py
```
Your browser should open the local Streamlit app.

## 5. Enable live Gemini generation (optional)
1. Create an API key in [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.env.example` and rename the copy to `.env`.
3. Open `.env` and replace the placeholder:
```env
GEMINI_API_KEY=your_actual_key
```
4. Stop and restart Streamlit.

Keep `.env` private. Do not upload it to GitHub or share your API key.

## How it works
1. The user enters lyrics and selects mood, genre and art style.
2. With a Gemini API key, the app sends a structured creative brief request to Gemini.
3. Gemini returns JSON containing the interpretation, title, colour palette, visual elements, sound direction and image prompt.
4. Without a key, the app uses a small built-in demo engine so the interface remains usable.

## Suggested project explanation for a viva
**Problem:** Musicians and creators may have lyrics but struggle to translate their emotional meaning into a consistent visual and sonic identity.

**Solution:** AI Music Studio uses a generative language model to interpret a lyric excerpt and propose a cohesive creative direction.

**GenAI component:** Gemini generates original structured text outputs from a user prompt. The application parses the response as JSON and displays each part in a dashboard.

**Tech stack:** Python, Streamlit, Google GenAI SDK, python-dotenv, JSON.

**Future scope:** Add actual image generation, audio upload and BPM/key detection with Librosa, lyric section detection, and export to PDF.
