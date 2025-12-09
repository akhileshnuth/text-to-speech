# tts_engine.py
import os
import uuid
import time

import pyttsx3
from gtts import gTTS

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


def list_voices():
    """
    Returns a list of available voices as dicts:
    { 'id': str, 'name': str, 'language': str }

    On environments where pyttsx3 cannot initialize (e.g. Streamlit Cloud Linux
    without espeak), this will return an empty list instead of crashing.
    """
    try:
        engine = pyttsx3.init()
    except Exception:
        # pyttsx3 not usable on this platform (e.g., missing espeak)
        return []

    voices = engine.getProperty("voices")
    voice_list = []

    for v in voices:
        lang = ""
        try:
            if getattr(v, "languages", None):
                first = v.languages[0]
                if isinstance(first, (bytes, bytearray)):
                    lang = first.decode(errors="ignore")
                else:
                    lang = str(first)
        except Exception:
            lang = ""
        voice_list.append(
            {
                "id": v.id,
                "name": v.name,
                "language": lang,
            }
        )

    engine.stop()
    return voice_list


# ---------- ENGINE IMPLEMENTATIONS ----------

def _tts_pyttsx3(text: str,
                 voice_id: str | None = None,
                 rate: int | None = None,
                 volume: float | None = None) -> str:
    """Offline TTS using pyttsx3. Raises RuntimeError if engine is unavailable."""
    try:
        engine = pyttsx3.init()
    except Exception as e:
        raise RuntimeError("Offline TTS (pyttsx3) is not available on this server.") from e

    if voice_id:
        engine.setProperty("voice", voice_id)

    if rate is not None:
        engine.setProperty("rate", int(rate))

    if volume is not None:
        volume = max(0.0, min(1.0, float(volume)))
        engine.setProperty("volume", volume)

    filename = f"{uuid.uuid4().hex}.mp3"
    output_path = os.path.join(AUDIO_DIR, filename)

    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

    return output_path


def _tts_gtts(text: str, lang: str = "en", tld: str = "com") -> str:
    """
    Google TTS via gTTS (online, more natural voice).
    'lang' chooses the language.
    'tld' chooses the accent for supported languages (like English).
    """
    filename = f"{uuid.uuid4().hex}.mp3"
    output_path = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang=lang, tld=tld)
    tts.save(output_path)

    return output_path


def text_to_speech_file(
    text: str,
    engine_name: str = "pyttsx3",
    voice_id: str | None = None,
    rate: int | None = None,
    volume: float | None = None,
    lang: str = "en",
    tld: str = "com",
) -> str:
    """
    Main entry point for TTS.
    engine_name: "pyttsx3" (offline) or "gtts" (Google TTS).
    For gTTS, voice_id/rate/volume are ignored; lang+tld control the voice.
    """
    engine_name = engine_name.lower()
    if engine_name == "gtts":
        return _tts_gtts(text, lang=lang, tld=tld)
    else:
        return _tts_pyttsx3(text, voice_id=voice_id, rate=rate, volume=volume)


# ---------- CLEANUP ----------

def clean_old_audio_files(max_age_minutes: int = 30) -> None:
    """Delete audio files older than max_age_minutes from AUDIO_DIR."""
    now = time.time()
    max_age_seconds = max_age_minutes * 60

    if not os.path.isdir(AUDIO_DIR):
        return

    for fname in os.listdir(AUDIO_DIR):
        fpath = os.path.join(AUDIO_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            age = now - os.path.getmtime(fpath)
            if age > max_age_seconds:
                os.remove(fpath)
        except OSError:
            pass
