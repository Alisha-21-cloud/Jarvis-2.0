# 🤖 JARVIS-2.0 - Your Personal AI Assistant

JARVIS-2.0 is a voice-controlled AI assistant built with Natural Language Processing, Deep Learning, and real-time voice synthesis using the ElevenLabs API. This project can understand user queries through speech, respond intelligently using an intent-based chatbot, and speak responses aloud using high-quality AI-generated voice.

---

## 🚀 Features

- 🎤 Voice recognition using `speech_recognition`
- 🧠 Intent-based NLP chatbot using TensorFlow model
- 🗣️ AI voice output using ElevenLabs API
- 🔐 Secure API key management via `.env`
- 🧪 Model training, testing, and inference capabilities
- 📂 Organized project structure with modular scripts

---

## 📁 Project Structure

```bash
JARVIS-2.0/
│
├── venv/                     # Virtual environment (excluded from GitHub)
├── .env                      # Stores ElevenLabs API Key (not committed)
├── .gitignore                # Ignores venv/, .env, and model files
│
├── main.py                   # Main entry point – runs the voice assistant
├── model_train.py            # Script to train the intent classification model
├── model_test.py             # Script to test the trained model manually
│
├── intents.json              # Predefined tags, patterns, and responses
├── chat_model.h5             # Trained Keras model
├── tokenizer.pkl             # Tokenizer for input vectorization
├── label_encoder.pkl         # Label encoder for intent classification
```

---

## 📦 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/JARVIS-2.0.git
cd JARVIS-2.0
```

2. **Create Virtual Environment**

```bash
python -m venv venv
```

3. **Activate Virtual Environment**

- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

5. **Add `.env` file**

Create a `.env` file in the root directory and add your ElevenLabs API key:

```env
ELEVEN_API_KEY=your_api_key_here
```

---

## 🛠 Usage

To start the JARVIS assistant:

```bash
python main.py
```

You can then speak to the assistant and receive intelligent, spoken responses.

---

## 🧠 Training the Model (Optional)

If you make changes to `intents.json`, re-train the model:

```bash
python model_train.py
```

---

## 🧪 Testing the Model (Optional)

Manually test the trained model:

```bash
python model_test.py
```

---

## 🔐 Environment Security

Ensure `.env` and model files are excluded from Git tracking using `.gitignore`.

---

## 📋 Example Intents (`intents.json`)

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey"],
      "responses": ["Hello!", "Hi there!", "Hey! How can I assist you?"]
    }
  ]
}
```

---

## 🗣 Voice Engine

This project uses [ElevenLabs](https://www.elevenlabs.io/) for high-quality AI speech synthesis. It is more natural and expressive than built-in TTS engines like `pyttsx3`.

---

## 💡 Future Improvements

- Add GUI using Tkinter or PyQt
- Integrate with APIs like Weather, News, and Calendar
- Add memory-based context for follow-up queries
- Face recognition-based user login (already planned)

---


## 👨‍💻 Author

Syed Ahmad Alisha  
📧 Feel free to connect and collaborate!
