# AI Health & Wellness Assistant

A comprehensive Python desktop application that provides AI-powered health information and guidance using the BLOOMZ-560M language model. The application supports both English and Marathi languages, with text and speech interaction capabilities.

## ⚠️ CRITICAL SAFETY DISCLAIMER

**IMPORTANT: This application is NOT a substitute for professional medical advice.**

- **Not a Doctor**: The AI assistant is NOT a medical professional and cannot provide diagnoses, prescriptions, or medical treatment.
- **General Information Only**: All health information provided is for general knowledge and educational purposes only.
- **Always Consult Professionals**: For any health concerns, symptoms, or medical questions, ALWAYS consult a qualified healthcare provider.
- **Emergency Situations**: In case of medical emergencies, call emergency services immediately.

## 🚀 Features

- **AI-Powered Health Information**: Uses the BLOOMZ-560M model for intelligent health guidance
- **Bilingual Support**: English and Marathi language support
- **Multimodal Interaction**: Text input and speech recognition capabilities
- **Text-to-Speech**: Audio playback of responses for accessibility
- **Structured Output**: Organized, easy-to-read health information format
- **Modern GUI**: Clean, intuitive Tkinter-based user interface
- **Safety-First Design**: Built-in disclaimers and safety warnings

## 📋 Prerequisites

- Python 3.8 or higher
- Windows 10/11 (tested on Windows 10)
- Microphone for speech input
- Speakers/headphones for audio output
- Internet connection (for initial model download and speech recognition)

## 🛠️ Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd disease_assistance
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Some packages may require additional system dependencies:

- **PyAudio**: If installation fails, you may need to install Microsoft Visual C++ Build Tools
- **torch**: The first run will download the AI model (~1.1GB)

### 3. Alternative Installation for PyAudio Issues
If PyAudio installation fails on Windows, try:
```bash
pip install pipwin
pipwin install pyaudio
```

## 🚀 Usage

### Starting the Application
```bash
python main.py
```

### Using the Application

1. **Language Selection**: Choose between English and Marathi from the dropdown menu
2. **Text Input**: Type your health-related question in the text field and press Enter or click Send
3. **Speech Input**: Click the "🎤 Speak" button and speak your question
4. **Reading Responses**: The AI will provide structured health information with safety disclaimers
5. **Audio Playback**: If you used speech input, the response will automatically be converted to audio

### Example Queries

**English:**
- "I have a headache, what should I do?"
- "What are the symptoms of common cold?"
- "How to treat minor cuts?"

**Marathi:**
- "मला डोकेदुखी आहे, काय करावे?"
- "सर्दीची लक्षणे काय आहेत?"
- "लहान कट कसे उपचार करावे?"

## 🔒 Safety Features

### Built-in Safety Measures
- **Mandatory Disclaimers**: Every response begins with a clear safety disclaimer
- **Scope Limitation**: Focuses on common, non-life-threatening conditions
- **Professional Consultation**: Always advises consulting healthcare professionals
- **Emergency Guidance**: Provides clear indicators for when to seek immediate medical help

### Response Structure
Each AI response follows a structured format:
- Disease/Condition Name
- **Safety Disclaimer** (prominently displayed)
- Overview of the condition
- Common symptoms
- General home care guidance
- When to consult a doctor

## 🏗️ Technical Architecture

### Core Components
- **GUI Framework**: Tkinter for cross-platform desktop interface
- **AI Model**: Hugging Face Transformers with BLOOMZ-560M
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: Google Text-to-Speech (gTTS)
- **Audio Playback**: Pygame for cross-platform audio support

### Model Information
- **Model**: bigscience/bloomz-560M
- **Size**: ~1.1GB (downloaded automatically on first run)
- **Capabilities**: Multilingual text generation with health domain knowledge
- **Performance**: Optimized for local inference with reasonable response times

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure stable internet connection for initial download
   - Check available disk space (minimum 2GB free)
   - Restart application if download fails

2. **Speech Recognition Issues**
   - Check microphone permissions
   - Ensure microphone is working in other applications
   - Verify internet connection for Google Speech API

3. **Audio Playback Problems**
   - Check speaker/headphone connections
   - Verify system audio settings
   - Restart application if pygame initialization fails

4. **PyAudio Installation Issues**
   - Install Microsoft Visual C++ Build Tools
   - Use pipwin: `pip install pipwin && pipwin install pyaudio`
   - Try pre-compiled wheels from unofficial sources

### Performance Optimization
- First run may be slower due to model download
- Subsequent runs will be faster with cached model
- Speech recognition requires stable internet connection

## 📁 Project Structure

```
disease_assistance/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## 🤝 Contributing

This project is designed for educational and research purposes. Contributions should focus on:
- Improving safety features
- Enhancing user experience
- Bug fixes and performance improvements
- Additional language support

## 📄 License

This project is provided as-is for educational purposes. Users are responsible for understanding and following all safety guidelines.

## ⚡ Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python main.py`
3. Select language and start asking health questions
4. **Remember**: Always consult healthcare professionals for medical advice

## 🔗 Additional Resources

- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [BLOOMZ Model Information](https://huggingface.co/bigscience/bloomz-560m)
- [Speech Recognition Documentation](https://pypi.org/project/SpeechRecognition/)
- [Google Text-to-Speech](https://pypi.org/project/gTTS/)

---

**Disclaimer**: This application is for educational purposes only. It is not intended to provide medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.
