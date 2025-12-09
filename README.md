
#  Text-to-Speech (TTS) Web Application

A feature-rich **Text-to-Speech (TTS)** system built using **Python**, **Streamlit**, **pyttsx3**, and **Google TTS (gTTS)**.  
Users can type text, customize voices, select engines, generate speech, listen to the output, download audio, and access a history of past conversions.

---

##  Features

###  1. Multiple TTS Engines
- **Offline Engine (pyttsx3)**  
  - Supports male/female voices  
  - Supports system accents  
  - Adjustable speech rate and volume  
- **Online Engine (Google gTTS)**  
  - High-quality natural voice output  
  - Supports multiple languages  
  - Supports English regional accents (via TLD)

---

##  Multi-Language Support (gTTS)

The application supports natural voice output in several Indian and global languages:
 Language       Code 
 **English**    `en` 
 **Hindi**      `hi` 
 **Telugu**     `te` 
 **Tamil**      `ta` 
 **Kannada**    `kn` 
 **Malayalam**  `ml` 
 **Marathi**    `mr` 
 **Gujarati**   `gu` 
 **Spanish**    `es` 
 **French**     `fr` 

Users can select any language directly from the sidebar.

---

##  English Accent Support (gTTS)

English has several accent options using the `tld` (top-level domain) parameter:

 Accent              TLD       Region          
 **Default**        `com`     Standard English 
 **India**          `co.in`   Indian English  
 **United States**  `com`     American English 
 **United Kingdom** `co.uk`   British English 
 **Australia**      `com.au`  Australian English 

Example:

```python
gTTS(text="Hello", lang="en", tld="co.uk")
```

---

##  Offline Voice Customization (pyttsx3)

- Choose male/female voices  
- Choose system-installed accents  
- Adjust speech **rate**  
- Adjust **volume**

This engine works fully offline.

---

##  Text Validation

The app performs input validation to ensure safe and clean speech generation:

- Removes control characters  
- Prevents empty or invalid inputs  
- Restricts overly long text  
- Includes complete **pytest unit tests**

---

## 🖥 Streamlit Web Application

Features include:

- Clean, modern UI  
- Sidebar controls for engine, language, accent, voice, rate, and volume  
- Audio player  
- Download button  
- Automatic file cleanup  
- Full **History** section to replay or download previous outputs  

---

##  Project Structure

```
Text-to-Speech/
│── app.py                 # Streamlit Web App
│── tts_engine.py          # TTS logic (pyttsx3 + gTTS)
│── validation.py          # Text validation
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
│── audio/                 # Generated audio files
│
└── tests/
    └── test_validation.py # Unit tests
```

---

##  Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

---

##  Run the Application

```bash
streamlit run app.py
```

The app runs at:

```
http://localhost:8501
```

---

##  Usage

1. Select TTS engine  
2. Choose language (gTTS) or voice (pyttsx3)  
3. Set speech rate & volume (offline only)  
4. Enter text  
5. Click **Generate Speech**  
6. Listen & download output  
7. Review past results in History  

---

##  Running Tests

```bash
pytest
```

---

##  Technologies Used

- Python 3  
- Streamlit  
- pyttsx3  
- gTTS  
- PyTest  

---

##  Contributing

Pull requests and suggestions are welcome!

---

##  License

This project is free for educational and personal use.
