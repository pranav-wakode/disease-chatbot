import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import pygame
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from datetime import datetime
import queue

class HealthAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Health & Wellness Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.current_language = "English"
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Initialize model (will be loaded in background)
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        # Start model loading in background
        threading.Thread(target=self.load_model, daemon=True).start()
        
        self.setup_ui()
        self.setup_audio_thread()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="AI Health & Wellness Assistant", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Language selector
        lang_frame = tk.Frame(main_frame, bg='#f0f0f0')
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        lang_label = tk.Label(lang_frame, text="Language:", bg='#f0f0f0', font=('Arial', 10))
        lang_label.pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value="English")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 values=["English", "Marathi"], state="readonly", width=15)
        lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Chat display area
        chat_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                     font=('Arial', 10), bg='white', fg='#2c3e50')
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_field = tk.Entry(input_frame, font=('Arial', 11), bg='white', fg='#2c3e50')
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind('<Return>', self.send_message)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message,
                                   bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                   relief=tk.FLAT, padx=20, pady=5)
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.speak_button = tk.Button(button_frame, text="🎤 Speak", command=self.start_speech_recognition,
                                    bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT, padx=20, pady=5)
        self.speak_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                            bg='#ecf0f1', fg='#7f8c8d', font=('Arial', 9))
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Welcome message
        self.add_message("System", "Welcome to your AI Health & Wellness Assistant! Please select your preferred language and ask me about common health concerns. Remember, I provide general information only - always consult a doctor for medical advice.", "system")
    
    def setup_audio_thread(self):
        """Setup thread for handling audio playback"""
        def audio_worker():
            while True:
                try:
                    audio_file = self.audio_queue.get()
                    if audio_file and os.path.exists(audio_file):
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        # Clean up temporary file
                        try:
                            os.remove(audio_file)
                        except:
                            pass
                except Exception as e:
                    print(f"Audio playback error: {e}")
                finally:
                    self.audio_queue.task_done()
        
        threading.Thread(target=audio_worker, daemon=True).start()
    
    def load_model(self):
        """Load the BLOOMZ model in background"""
        try:
            self.status_var.set("Loading AI model... Please wait...")
            self.root.update()
            
            model_name = "bigscience/bloomz-560m"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            self.model_loaded = True
            self.status_var.set("AI model loaded successfully!")
            self.root.update()
            
        except Exception as e:
            self.status_var.set(f"Error loading model: {str(e)}")
            messagebox.showerror("Error", f"Failed to load AI model: {str(e)}")
    
    def on_language_change(self, event=None):
        """Handle language change"""
        self.current_language = self.lang_var.get()
        self.add_message("System", f"Language changed to {self.current_language}", "system")
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n\n")
        elif msg_type == "assistant":
            self.chat_display.insert(tk.END, f"[{timestamp}] AI Assistant: {message}\n\n")
        elif msg_type == "system":
            self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n\n")
        
        self.chat_display.see(tk.END)
        self.root.update()
    
    def send_message(self, event=None):
        """Send text message"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message("You", message, "user")
        
        # Process message in background
        threading.Thread(target=self.process_message, args=(message, False), daemon=True).start()
    
    def start_speech_recognition(self):
        """Start speech recognition"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.speak_button.config(text="🔴 Listening...", bg='#e67e22')
        self.status_var.set("Listening... Speak now!")
        
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Convert speech to text
            language = "en-IN" if self.current_language == "English" else "mr-IN"
            text = self.recognizer.recognize_google(audio, language=language)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.handle_speech_result(text))
            
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.handle_speech_result(""))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.handle_speech_result(""))
        except Exception as e:
            self.root.after(0, lambda: self.handle_speech_result(""))
        finally:
            self.root.after(0, self.reset_speech_ui)
    
    def handle_speech_result(self, text):
        """Handle speech recognition result"""
        if text:
            self.add_message("You", f"You said: {text}", "user")
            # Process speech input
            threading.Thread(target=self.process_message, args=(text, True), daemon=True).start()
        else:
            self.add_message("System", "Could not understand speech. Please try again.", "system")
    
    def reset_speech_ui(self):
        """Reset speech UI elements"""
        self.is_listening = False
        self.speak_button.config(text="🎤 Speak", bg='#e74c3c')
        self.status_var.set("Ready")
    
    def process_message(self, message, was_speech):
        """Process user message and generate response"""
        if not self.model_loaded:
            self.add_message("System", "AI model is still loading. Please wait...", "system")
            return
        
        try:
            # Construct prompt for the model
            prompt = self.construct_prompt(message)
            
            # Generate response
            response = self.generate_response(prompt)
            
            # Parse and format response
            formatted_response = self.parse_response(response)
            
            # Display response
            self.root.after(0, lambda: self.add_message("AI Assistant", formatted_response, "assistant"))
            
            # Generate audio if input was speech
            if was_speech:
                self.root.after(0, lambda: self.generate_audio_response(formatted_response))
                
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, lambda: self.add_message("System", error_msg, "system"))
    
    def construct_prompt(self, user_query):
        """Construct prompt for the BLOOMZ model"""
        if self.current_language == "English":
            disclaimer = "DISCLAIMER: I am an AI assistant, not a medical professional. This information is for general knowledge only. Please consult a qualified doctor for any health concerns."
            prompt = f"""You are a helpful AI health assistant. A user has asked: '{user_query}'. 

Provide a structured response about common health conditions. The response must strictly follow this format:

**Disease Name:** [Identified Ailment]

**Disclaimer:** {disclaimer}

**Overview:** [A brief, simple 1-2 sentence explanation of the condition.]

**Common Symptoms:**
- Symptom 1
- Symptom 2
- Symptom 3

**General Home Care & Guidance:** [Safe, general, non-prescriptive advice. E.g., "Rest," "Stay hydrated," "Warm salt water gargle."]

**When to Consult a Doctor:** [Clear indicators for seeking professional help. E.g., "If symptoms persist for more than 5 days," "If you have a high fever," "If you experience difficulty breathing."]

Focus on common, non-life-threatening conditions. For severe conditions, provide basic information and strongly advise seeing a doctor immediately."""
        else:
            disclaimer = "अस्वीकरण: मी एक AI सहाय्यक आहे, वैद्यकीय व्यावसायिक नाही. ही माहिती केवळ सामान्य ज्ञानासाठी आहे. कृपया कोणत्याही आरोग्यविषयक समस्यांसाठी पात्र डॉक्टरांचा सल्ला घ्या."
            prompt = f"""You are a helpful AI health assistant. A user has asked in Marathi: '{user_query}'. 

Provide a structured response in Marathi for common health conditions. The response must strictly follow this format:

**रोगाचे नाव:** [Identified Ailment]

**अस्वीकरण:** {disclaimer}

**सर्वसाधारण माहिती:** [A brief, simple 1-2 sentence explanation of the condition in Marathi.]

**सामान्य लक्षणे:**
- लक्षण 1
- लक्षण 2
- लक्षण 3

**सामान्य घरगुती काळजी आणि मार्गदर्शन:** [Safe, general, non-prescriptive advice in Marathi.]

**डॉक्टरांना कधी भेटावे:** [Clear indicators for seeking professional help in Marathi.]

Focus on common, non-life-threatening conditions. For severe conditions, provide basic information and strongly advise seeing a doctor immediately."""
        
        return prompt
    
    def generate_response(self, prompt):
        """Generate response using BLOOMZ model"""
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=1024,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (remove the input prompt)
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            raise Exception(f"Model inference error: {str(e)}")
    
    def parse_response(self, response):
        """Parse and format the model response"""
        # Clean up the response
        response = response.strip()
        
        # If response is empty or too short, provide a default response
        if len(response) < 50:
            if self.current_language == "English":
                return """**Disease Name:** General Health Inquiry

**Disclaimer:** DISCLAIMER: I am an AI assistant, not a medical professional. This information is for general knowledge only. Please consult a qualified doctor for any health concerns.

**Overview:** I understand you have a health-related question, but I need more specific information to provide helpful guidance.

**Common Symptoms:** Please describe your symptoms in detail.

**General Home Care & Guidance:** For general wellness, maintain a healthy lifestyle with proper diet, exercise, and rest.

**When to Consult a Doctor:** If you have persistent symptoms, pain, or concerns about your health, please consult a healthcare professional."""
            else:
                return """**रोगाचे नाव:** सामान्य आरोग्य विचारणा

**अस्वीकरण:** अस्वीकरण: मी एक AI सहाय्यक आहे, वैद्यकीय व्यावसायिक नाही. ही माहिती केवळ सामान्य ज्ञानासाठी आहे. कृपया कोणत्याही आरोग्यविषयक समस्यांसाठी पात्र डॉक्टरांचा सल्ला घ्या.

**सर्वसाधारण माहिती:** मला तुमच्या आरोग्याशी संबंधित प्रश्न समजतो, पण मदतकारक मार्गदर्शन देण्यासाठी मला अधिक विशिष्ट माहिती हवी आहे.

**सामान्य लक्षणे:** कृपया तुमची लक्षणे तपशीलवार वर्णन करा.

**सामान्य घरगुती काळजी आणि मार्गदर्शन:** सामान्य आरोग्यासाठी, योग्य आहार, व्यायाम आणि विश्रांतीसह निरोगी जीवनशैली राखा.

**डॉक्टरांना कधी भेटावे:** जर तुम्हाला सतत लक्षणे, वेदना किंवा तुमच्या आरोग्याबद्दल काळजी असेल तर कृपया आरोग्य सेवा व्यावसायिकांचा सल्ला घ्या."""
        
        return response
    
    def generate_audio_response(self, text_response):
        """Generate audio from text response and play it"""
        try:
            # Extract key sections for audio
            lines = text_response.split('\n')
            audio_text = ""
            
            for line in lines:
                if line.strip() and not line.startswith('**') and not line.startswith('-'):
                    audio_text += line.strip() + ". "
            
            if not audio_text:
                return
            
            # Generate audio file
            language = "en" if self.current_language == "English" else "mr"
            tts = gTTS(text=audio_text, lang=language, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                self.audio_queue.put(tmp_file.name)
                
        except Exception as e:
            print(f"Audio generation error: {e}")

def main():
    root = tk.Tk()
    app = HealthAssistantApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()
