#!/usr/bin/env python3
"""
Demo script for the AI Health & Wellness Assistant
This script demonstrates the core functionality without the GUI
Useful for testing the AI model and speech capabilities
"""

import os
import sys
import time
from datetime import datetime

def print_header():
    """Print application header"""
    print("=" * 60)
    print("🤖 AI Health & Wellness Assistant - Demo Mode")
    print("=" * 60)
    print("This demo showcases the core AI capabilities")
    print("⚠️  REMEMBER: This is NOT a medical device!")
    print("=" * 60)
    print()

def test_model_loading():
    """Test if the AI model can be loaded"""
    print("🔍 Testing AI Model Loading...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print("✅ Transformers and PyTorch imported successfully")
        
        # Check if model is already downloaded
        model_name = "bigscience/bloomz-560m"
        cache_dir = os.path.expanduser("~/.cache/huggingface")
        
        if os.path.exists(cache_dir):
            print("✅ Hugging Face cache directory found")
        else:
            print("📁 Hugging Face cache directory will be created")
        
        print("⏳ Loading AI model (this may take a few minutes on first run)...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print("✅ AI model loaded successfully!")
        return tokenizer, model
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return None, None
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return None, None

def test_text_generation(tokenizer, model):
    """Test text generation capabilities"""
    if not tokenizer or not model:
        print("❌ Cannot test text generation - model not loaded")
        return
    
    print("\n📝 Testing Text Generation...")
    
    # Test prompts
    test_prompts = [
        "I have a headache, what should I do?",
        "What are the symptoms of common cold?",
        "How to treat minor cuts and scrapes?"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}: {prompt} ---")
        
        try:
            # Construct a simple prompt
            full_prompt = f"""You are a helpful AI health assistant. A user has asked: '{prompt}'. 

Provide a brief, structured response about this health topic. Include a safety disclaimer and focus on general information only.

Response:"""
            
            # Generate response
            inputs = tokenizer.encode(full_prompt, return_tensors="pt", max_length=256, truncation=True)
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=512,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part
            if response.startswith(full_prompt):
                response = response[len(full_prompt):].strip()
            
            print("AI Response:")
            print(response[:300] + "..." if len(response) > 300 else response)
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
        
        time.sleep(1)  # Brief pause between generations

def test_speech_recognition():
    """Test speech recognition capabilities"""
    print("\n🎤 Testing Speech Recognition...")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("✅ Speech recognition libraries imported")
        print("📱 Microphone access available")
        
        # Test microphone
        with microphone as source:
            print("🔇 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone configured")
        
        return True
        
    except ImportError:
        print("❌ Speech recognition not available")
        print("Install with: pip install SpeechRecognition PyAudio")
        return False
    except Exception as e:
        print(f"❌ Speech recognition error: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech capabilities"""
    print("\n🔊 Testing Text-to-Speech...")
    
    try:
        from gtts import gTTS
        import tempfile
        import pygame
        
        print("✅ gTTS and pygame imported")
        
        # Test TTS generation
        test_text = "Hello, this is a test of the text to speech system."
        tts = gTTS(text=test_text, lang='en', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            print(f"✅ Audio file generated: {tmp_file.name}")
            
            # Clean up
            try:
                os.remove(tmp_file.name)
                print("✅ Temporary file cleaned up")
            except:
                pass
        
        return True
        
    except ImportError:
        print("❌ Text-to-speech not available")
        print("Install with: pip install gTTS pygame")
        return False
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def run_interactive_demo(tokenizer, model):
    """Run an interactive demo session"""
    if not tokenizer or not model:
        print("❌ Cannot run interactive demo - model not loaded")
        return
    
    print("\n🎯 Interactive Demo Mode")
    print("Type your health questions (or 'quit' to exit)")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n🤔 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Demo ended. Thanks for trying!")
                break
            
            if not user_input:
                continue
            
            print("⏳ Generating response...")
            
            # Generate response
            prompt = f"""You are a helpful AI health assistant. A user has asked: '{user_input}'. 

Provide a structured response about this health topic. Include a safety disclaimer and focus on general information only.

Response:"""
            
            inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=256, truncation=True)
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=512,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            print("\n🤖 AI Response:")
            print("-" * 30)
            print(response)
            print("-" * 30)
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Thanks for trying!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    print_header()
    
    # Test model loading
    tokenizer, model = test_model_loading()
    
    if not tokenizer or not model:
        print("\n❌ Demo cannot continue without the AI model")
        print("Please check your installation and try again")
        return
    
    # Test other capabilities
    speech_available = test_speech_recognition()
    tts_available = test_text_to_speech()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Demo Test Results:")
    print("=" * 60)
    print(f"✅ AI Model: Loaded successfully")
    print(f"{'✅' if speech_available else '❌'} Speech Recognition: {'Available' if speech_available else 'Not available'}")
    print(f"{'✅' if tts_available else '❌'} Text-to-Speech: {'Available' if tts_available else 'Not available'}")
    print("=" * 60)
    
    # Interactive demo
    if input("\n🎯 Would you like to try the interactive demo? (y/n): ").lower().startswith('y'):
        run_interactive_demo(tokenizer, model)
    
    print("\n🎉 Demo completed!")
    print("To run the full application with GUI, use: python main.py")

if __name__ == "__main__":
    main()
