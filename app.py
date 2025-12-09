# app.py
import os
from datetime import datetime

import streamlit as st

from tts_engine import list_voices, text_to_speech_file, clean_old_audio_files
from validation import clean_and_validate_text, ValidationError


@st.cache_resource
def get_voices():
    return list_voices()


def init_history():
    if "history" not in st.session_state:
        st.session_state["history"] = []


# Languages for gTTS (you can extend this dict later)
GTTs_LANG_OPTIONS = {
    "English": {"lang": "en"},
    "Hindi": {"lang": "hi"},
    "Telugu": {"lang": "te"},
    "Tamil": {"lang": "ta"},
    "Kannada": {"lang": "kn"},
    "Malayalam": {"lang": "ml"},
    "Marathi": {"lang": "mr"},
    "Gujarati": {"lang": "gu"},
    "Spanish": {"lang": "es"},
    "French": {"lang": "fr"},
}

# Mapping of English accents -> tld for gTTS
ENGLISH_ACCENT_TLD = {
    "Default": "com",       # generic
    "India": "co.in",       # Indian English
    "US": "com",            # American English (default)
    "UK": "co.uk",          # British English
    "Australia": "com.au",  # Australian English
}


def main():
    st.set_page_config(page_title="Text-to-Speech (TTS)", page_icon="🗣️")

    st.title("🗣️ Text-to-Speech Converter")
    st.write(
        "Convert your text into speech with customizable **engine**, "
        "**voice**, **rate**, and **volume**. Generated audio is saved in "
        "the **history** so you can replay or download it later."
    )

    init_history()
    voices = get_voices()
    pyttsx3_available = len(voices) > 0

    # ---------------- Sidebar: engine & settings ----------------
    st.sidebar.header("Settings")

    # Build engine options based on availability
    engine_options = []
    if pyttsx3_available:
        engine_options.append("Offline (pyttsx3)")
    engine_options.append("Google TTS (gTTS)")

    engine_choice = st.sidebar.selectbox(
        "TTS Engine",
        engine_options,
    )

    engine_name = "pyttsx3" if engine_choice.startswith("Offline") else "gtts"

    if not pyttsx3_available and engine_name == "pyttsx3":
        st.sidebar.warning(
            "Offline TTS (pyttsx3) is not available on this server. "
            "Please switch to Google TTS (gTTS)."
        )

    # ---------- gTTS language & accent (only when Google TTS is selected) ----------
    gtts_lang = "en"
    gtts_tld = "com"

    if engine_name == "gtts":
        st.sidebar.subheader("Language (gTTS)")
        language_names = list(GTTs_LANG_OPTIONS.keys())
        selected_lang_name = st.sidebar.selectbox(
            "Language",
            language_names,
        )
        gtts_lang = GTTs_LANG_OPTIONS[selected_lang_name]["lang"]

        # English accents via tld
        if selected_lang_name == "English":
            accent = st.sidebar.selectbox(
                "English Accent",
                ["Default", "India", "US", "UK", "Australia"],
            )
            gtts_tld = ENGLISH_ACCENT_TLD[accent]
        else:
            # For other languages, default tld 'com' works fine
            gtts_tld = "com"

        st.sidebar.info(
            "gTTS uses a single voice per language. "
            "Rate, volume, and offline voice settings do not affect gTTS."
        )

    # ---------- Voice selection: ONLY for offline engine ----------
    selected_voice_id = None

    if engine_name == "pyttsx3" and pyttsx3_available:
        voice_options = ["Default"] + [
            f"{v['name']} ({v['language']})" if v["language"] else v["name"]
            for v in voices
        ]
        selected_voice_label = st.sidebar.selectbox(
            "Voice (offline only)", voice_options
        )

        if selected_voice_label != "Default":
            index = voice_options.index(selected_voice_label) - 1
            selected_voice_id = voices[index]["id"]
    elif engine_name == "pyttsx3":
        st.sidebar.info(
            "Offline voices are not available on this server. "
            "Please use Google TTS (gTTS)."
        )
    else:
        st.sidebar.info(
            "Voice selection is only available for the Offline (pyttsx3) engine."
        )

    # Speech rate + volume (only applied for pyttsx3)
    rate = st.sidebar.slider(
        "Speech rate (words/min, offline only)",
        min_value=100,
        max_value=300,
        value=200,
        step=10,
    )
    volume = st.sidebar.slider(
        "Volume (offline only)",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.1,
    )

    # ---------------- Main layout ----------------
    col_text, col_output = st.columns([2, 1])

    audio_path = None
    cleaned_text = ""

    with col_text:
        with st.form(key="tts_form"):
            text_input = st.text_area(
                "Enter text here:",
                height=220,
                placeholder="Type or paste the text you want to convert to speech...",
            )
            submitted = st.form_submit_button("Generate Speech")

        if submitted:
            try:
                clean_old_audio_files(max_age_minutes=30)
                cleaned_text = clean_and_validate_text(text_input)

                audio_path = text_to_speech_file(
                    cleaned_text,
                    engine_name=engine_name,
                    voice_id=selected_voice_id,
                    rate=rate,
                    volume=volume,
                    lang=gtts_lang,
                    tld=gtts_tld,
                )

                # Save to history (newest first)
                st.session_state["history"].insert(
                    0,
                    {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "engine": engine_choice,
                        "text": cleaned_text,
                        "audio_path": audio_path,
                        "lang": gtts_lang if engine_name == "gtts" else None,
                    },
                )

                st.success("Audio generated successfully!")

            except ValidationError as ve:
                st.error(f"Validation error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    # ---------------- Current audio preview ----------------
    with col_output:
        if audio_path and os.path.exists(audio_path):
            st.subheader("Current Audio")
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="⬇️ Download Current Audio",
                data=audio_bytes,
                file_name=os.path.basename(audio_path),
                mime="audio/mpeg",
                key="download_current",
            )

    # ---------------- History section ----------------
    st.markdown("---")
    st.subheader("History")

    history = st.session_state.get("history", [])
    if not history:
        st.info("No audio generated yet.")
    else:
        for i, item in enumerate(history):
            label = f"{item['timestamp']} – {item['engine']}"
            with st.expander(label):
                st.caption("Text used:")
                st.text_area(
                    "Text",
                    value=item["text"],
                    height=120,
                    disabled=True,
                    key=f"text_hist_{i}",
                )

                path = item["audio_path"]
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        label="⬇️ Download",
                        data=audio_bytes,
                        file_name=os.path.basename(path),
                        mime="audio/mpeg",
                        key=f"download_hist_{i}",
                    )
                else:
                    st.warning("Audio file not found (it may have been cleaned).")


if __name__ == "__main__":
    main()
