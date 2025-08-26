"""
Configuration file for the AI Health & Wellness Assistant
Modify these settings to customize the application behavior
"""

# Application Settings
APP_NAME = "AI Health & Wellness Assistant"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# AI Model Configuration
MODEL_NAME = "bigscience/bloomz-560m"
MAX_INPUT_LENGTH = 512
MAX_OUTPUT_LENGTH = 1024
GENERATION_TEMPERATURE = 0.7
GENERATION_DO_SAMPLE = True

# Speech Recognition Settings
SPEECH_TIMEOUT = 5  # seconds
SPEECH_PHRASE_TIME_LIMIT = 10  # seconds
SPEECH_AMBIENT_NOISE_DURATION = 0.5  # seconds

# Language Settings
SUPPORTED_LANGUAGES = {
    "English": {
        "code": "en",
        "speech_code": "en-IN",
        "disclaimer": "DISCLAIMER: I am an AI assistant, not a medical professional. This information is for general knowledge only. Please consult a qualified doctor for any health concerns."
    },
    "Marathi": {
        "code": "mr",
        "speech_code": "mr-IN",
        "disclaimer": "अस्वीकरण: मी एक AI सहाय्यक आहे, वैद्यकीय व्यावसायिक नाही. ही माहिती केवळ सामान्य ज्ञानासाठी आहे. कृपया कोणत्याही आरोग्यविषयक समस्यांसाठी पात्र डॉक्टरांचा सल्ला घ्या."
    }
}

# UI Colors and Styling
COLORS = {
    "background": "#f0f0f0",
    "primary": "#3498db",
    "secondary": "#e74c3c",
    "warning": "#e67e22",
    "success": "#27ae60",
    "text_primary": "#2c3e50",
    "text_secondary": "#7f8c8d",
    "white": "#ffffff",
    "light_gray": "#ecf0f1"
}

# Font Settings
FONTS = {
    "title": ("Arial", 16, "bold"),
    "heading": ("Arial", 12, "bold"),
    "body": ("Arial", 10),
    "input": ("Arial", 11),
    "status": ("Arial", 9)
}

# Response Templates
RESPONSE_TEMPLATES = {
    "English": {
        "structure": [
            "**Disease Name:**",
            "**Disclaimer:**",
            "**Overview:**",
            "**Common Symptoms:**",
            "**General Home Care & Guidance:**",
            "**When to Consult a Doctor:**"
        ],
        "default_response": """**Disease Name:** General Health Inquiry

**Disclaimer:** DISCLAIMER: I am an AI assistant, not a medical professional. This information is for general knowledge only. Please consult a qualified doctor for any health concerns.

**Overview:** I understand you have a health-related question, but I need more specific information to provide helpful guidance.

**Common Symptoms:** Please describe your symptoms in detail.

**General Home Care & Guidance:** For general wellness, maintain a healthy lifestyle with proper diet, exercise, and rest.

**When to Consult a Doctor:** If you have persistent symptoms, pain, or concerns about your health, please consult a healthcare professional."""
    },
    "Marathi": {
        "structure": [
            "**रोगाचे नाव:**",
            "**अस्वीकरण:**",
            "**सर्वसाधारण माहिती:**",
            "**सामान्य लक्षणे:**",
            "**सामान्य घरगुती काळजी आणि मार्गदर्शन:**",
            "**डॉक्टरांना कधी भेटावे:**"
        ],
        "default_response": """**रोगाचे नाव:** सामान्य आरोग्य विचारणा

**अस्वीकरण:** अस्वीकरण: मी एक AI सहाय्यक आहे, वैद्यकीय व्यावसायिक नाही. ही माहिती केवळ सामान्य ज्ञानासाठी आहे. कृपया कोणत्याही आरोग्यविषयक समस्यांसाठी पात्र डॉक्टरांचा सल्ला घ्या.

**सर्वसाधारण माहिती:** मला तुमच्या आरोग्याशी संबंधित प्रश्न समजतो, पण मदतकारक मार्गदर्शन देण्यासाठी मला अधिक विशिष्ट माहिती हवी आहे.

**सामान्य लक्षणे:** कृपया तुमची लक्षणे तपशीलवार वर्णन करा.

**सामान्य घरगुती काळजी आणि मार्गदर्शन:** सामान्य आरोग्यासाठी, योग्य आहार, व्यायाम आणि विश्रांतीसह निरोगी जीवनशैली राखा.

**डॉक्टरांना कधी भेटावे:** जर तुम्हाला सतत लक्षणे, वेदना किंवा तुमच्या आरोग्याबद्दल काळजी असेल तर कृपया आरोग्य सेवा व्यावसायिकांचा सल्ला घ्या."""
    }
}

# Safety Settings
SAFETY = {
    "max_response_length": 2000,  # characters
    "min_response_length": 50,    # characters
    "forbidden_topics": [
        "prescription medication",
        "medical diagnosis",
        "treatment plans",
        "surgery",
        "emergency procedures"
    ],
    "emergency_keywords": [
        "chest pain",
        "difficulty breathing",
        "severe bleeding",
        "unconscious",
        "stroke",
        "heart attack"
    ]
}

# Audio Settings
AUDIO = {
    "sample_rate": 22050,
    "chunk_size": 1024,
    "format": "mp3",
    "playback_volume": 0.8
}

# Logging Settings
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "health_assistant.log"
}
