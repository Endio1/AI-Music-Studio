import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Music Studio", page_icon="🎧", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #100f1d 0%, #1d1830 55%, #111827 100%); color: #f5f3ff;}
[data-testid="stSidebar"] {background: #171528;}
.hero {padding: 1.5rem 1.7rem; border: 1px solid #51446f; border-radius: 22px;
background: linear-gradient(110deg, rgba(116,75,162,.30), rgba(45,125,145,.20));}
.hero h1 {font-size: 2.5rem; margin-bottom: .2rem;}
.small-muted {color: #c4b8dc;}
.result {padding: 1rem 1.2rem; border-radius: 15px; background: rgba(255,255,255,.06);
border: 1px solid rgba(255,255,255,.12); margin: .5rem 0 1rem 0;}
.tag {display:inline-block; padding:.25rem .65rem; margin:.2rem; border-radius:30px;
background:#382d54; color:#e9ddff; font-size:.85rem;}
</style>
""", unsafe_allow_html=True)

def fallback_creation(lyrics, mood, genre, style):
    words = [w.strip(".,!?;:()[]{}").lower() for w in lyrics.split()]
    words = [w for w in words if len(w) > 4]
    keywords = list(dict.fromkeys(words))[:6]
    palette_map = {
        "Dreamy": "lavender, midnight blue, silver and soft pink",
        "Melancholic": "deep indigo, muted teal, charcoal and dusty rose",
        "Energetic": "electric orange, neon magenta, cobalt and black",
        "Romantic": "rose pink, warm cream, burgundy and gold",
        "Hopeful": "sunrise amber, sky blue, peach and ivory",
        "Mysterious": "black, emerald, violet and moonlit silver",
    }
    palette = palette_map.get(mood, "violet, midnight blue, silver and warm amber")
    subject = ", ".join(keywords[:3]) if keywords else "a lone figure beneath a vast sky"
    return {
        "interpretation": f"The lyrics suggest a {mood.lower()} emotional journey, expressed through the imagery of {subject}. The arrangement could blend {genre.lower()} textures with a {style.lower()} visual language.",
        "visual_prompt": f"Create a {style.lower()} album-cover artwork inspired by these lyrics: {subject}. Mood: {mood.lower()}. Colour palette: {palette}. Cinematic composition, expressive lighting, layered symbolism, rich texture, no text, square album cover.",
        "title": "Echoes in the Afterglow",
        "palette": palette,
        "visual_elements": ["A symbolic central subject", "Atmospheric light and shadow", "Subtle lyric-inspired textures"],
        "sound_direction": f"{genre} with spacious layers, expressive dynamics and a {mood.lower()} atmosphere."
    }

def ask_gemini(lyrics, mood, genre, style, api_key):
    from google import genai
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are a creative music producer and album-art director.
Analyze the user-provided lyrics and create an original creative direction.
Mood: {mood}; Genre: {genre}; Art style: {style}.
Lyrics:
{lyrics}

Return ONLY valid JSON with these keys:
interpretation (2-3 sentences), visual_prompt (detailed image-generation prompt; no text in image),
title (short original track/album title), palette (4-6 colour palette),
visual_elements (array of 3-5 concise items), sound_direction (2 sentences).
Do not continue or reproduce the lyrics. Do not identify a real artist.
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    raw = response.text.strip()
    raw = raw.removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw)

st.markdown("""
<div class="hero">
  <h1>🎧 AI Music Studio</h1>
  <div class="small-muted">Turn lyrics into a complete creative universe — meaning, sound direction and album-art concepts.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Studio settings")
    mood = st.selectbox("Main mood", ["Dreamy", "Melancholic", "Energetic", "Romantic", "Hopeful", "Mysterious"])
    genre = st.selectbox("Music genre", ["Indie Pop", "Hip-Hop", "R&B", "Rock", "Electronic", "Lo-fi", "Acoustic", "Cinematic"])
    style = st.selectbox("Artwork style", ["Surrealism", "Anime-inspired illustration", "Minimalist", "Dreamlike photography", "Cyberpunk", "Watercolour", "3D digital art"])
    st.divider()
    st.caption("Optional: add a Gemini API key in a local .env file to enable live AI-generated creative analysis.")
    api_key = os.getenv("GEMINI_API_KEY", "")

left, right = st.columns([1.15, .85], gap="large")
with left:
    st.subheader("✍️ Your lyrics")
    lyrics = st.text_area("Paste a verse, chorus or your own lyrics", height=260,
        placeholder="Type or paste your lyrics here...\n\nTip: original lyrics work best.")
    st.caption("Use lyrics you wrote or have permission to use.")
    generate = st.button("✨ Generate my music universe", type="primary", use_container_width=True)

with right:
    st.subheader("What you'll get")
    st.markdown("""
    <div class="result">
    <h4>🧠 Lyric interpretation</h4><p class="small-muted">Themes, imagery and emotional direction.</p>
    <h4>🎨 Album-art prompt</h4><p class="small-muted">A detailed prompt to use in an image generator.</p>
    <h4>🎼 Sound direction</h4><p class="small-muted">Genre-aware production and atmosphere ideas.</p>
    <h4>💿 Creative identity</h4><p class="small-muted">A title, colour palette and visual motifs.</p>
    </div>
    """, unsafe_allow_html=True)

if generate:
    if len(lyrics.strip()) < 20:
        st.warning("Please enter at least a few lines of lyrics (20 characters or more).")
    else:
        with st.spinner("Composing your creative direction..."):
            try:
                if api_key:
                    data = ask_gemini(lyrics, mood, genre, style, api_key)
                    st.success("Generated with Gemini AI.")
                else:
                    data = fallback_creation(lyrics, mood, genre, style)
                    st.info("Showing the built-in demo engine. Add a Gemini API key to enable live generative AI.")
                st.session_state["creation"] = data
            except Exception as e:
                st.error(f"AI request failed, so the demo engine was used instead. Details: {e}")
                st.session_state["creation"] = fallback_creation(lyrics, mood, genre, style)

if "creation" in st.session_state:
    d = st.session_state["creation"]
    st.divider()
    st.header("Your generated music universe")
    st.markdown(f"## 💿 {d.get('title', 'Untitled')}")
    a, b = st.columns(2)
    with a:
        st.markdown("### 🧠 Lyric interpretation")
        st.write(d.get("interpretation", ""))
        st.markdown("### 🎼 Sound direction")
        st.write(d.get("sound_direction", ""))
    with b:
        st.markdown("### 🎨 Colour palette")
        st.markdown(f'<div class="result">{d.get("palette", "")}</div>', unsafe_allow_html=True)
        st.markdown("### ✨ Visual elements")
        for item in d.get("visual_elements", []):
            st.markdown(f"- {item}")
    st.markdown("### 🖼️ Album-art generation prompt")
    st.code(d.get("visual_prompt", ""), language="text")
    st.download_button("⬇️ Download creative brief (JSON)", data=json.dumps(d, indent=2),
        file_name="my_music_universe.json", mime="application/json")
    st.caption("The app creates an image prompt; it does not generate the artwork itself.")

st.divider()
st.caption("AI Music Studio • Student GenAI project • Built with Streamlit + optional Gemini API")
