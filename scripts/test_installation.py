#!/usr/bin/env python3
"""
Test script to verify installation of all required dependencies
Run this script to check if your environment is properly set up
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name)
            print(f"✅ {package_name} imported successfully")
            return True
        else:
            importlib.import_module(module_name)
            print(f"✅ {module_name} imported successfully")
            return True
    except ImportError as e:
        print(f"❌ Failed to import {package_name or module_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name or module_name} imported but with warning: {e}")
        return True

def main():
    print("🔍 Testing Health Assistant Dependencies...")
    print("=" * 50)
    
    # Core Python modules
    print("\n📦 Core Python Modules:")
    test_import("tkinter", "Tkinter")
    test_import("threading", "Threading")
    test_import("os", "OS")
    test_import("tempfile", "Tempfile")
    test_import("queue", "Queue")
    test_import("datetime", "Datetime")
    
    # AI and ML libraries
    print("\n🤖 AI and Machine Learning Libraries:")
    test_import("transformers", "Transformers")
    test_import("torch", "PyTorch")
    
    # Speech and Audio libraries
    print("\n🎤 Speech and Audio Libraries:")
    test_import("speech_recognition", "SpeechRecognition")
    test_import("gtts", "gTTS")
    test_import("pygame", "Pygame")
    
    # Additional utilities
    print("\n🛠️  Utility Libraries:")
    test_import("PIL", "Pillow")
    test_import("numpy", "NumPy")
    
    print("\n" + "=" * 50)
    print("🎯 Installation Test Complete!")
    print("\n📋 Next Steps:")
    print("1. If all modules imported successfully, you can run: python main.py")
    print("2. If there are import errors, run: pip install -r requirements.txt")
    print("3. For PyAudio issues on Windows, try: pip install pipwin && pipwin install pyaudio")
    print("\n⚠️  Remember: This is NOT a medical device. Always consult healthcare professionals.")

if __name__ == "__main__":
    main()
