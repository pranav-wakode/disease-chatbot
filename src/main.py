import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import pygame
from datetime import datetime
import queue

# --- NEW IMPORTS FOR GGUF MODEL ---
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

class HealthAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Health & Wellness Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.current_language = "English"
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        
        pygame.mixer.init()
        
        self.model = None # This will now be a Llama object
        self.model_loaded = False
        
        self.setup_ui()
        self.setup_audio_thread()

        threading.Thread(target=self.load_model, daemon=True).start()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="AI Health & Wellness Assistant", 
                               font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        lang_frame = tk.Frame(main_frame, bg='#f0f0f0')
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(lang_frame, text="Language:", bg='#f0f0f0', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value="English")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 values=["English", "Marathi"], state="readonly", width=15)
        lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        chat_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                     font=('Arial', 10), bg='white', fg='#2c3e50')
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_field = tk.Entry(input_frame, font=('Arial', 11), bg='white', fg='#2c3e50')
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind('<Return>', self.send_message)
        
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

        self.status_var = tk.StringVar()
        self.status_var.set("Welcome! Initializing AI model...")
        status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, wraplength=780)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.add_message("System", "Welcome to your AI Health & Wellness Assistant! Please select your preferred language and ask me about common health concerns. Remember, I provide general information only - always consult a doctor for medical advice.", "system")

    def setup_audio_thread(self):
        def audio_worker():
            while True:
                audio_file = self.audio_queue.get()
                if audio_file is None: break
                try:
                    if os.path.exists(audio_file):
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        pygame.mixer.music.unload()
                        os.remove(audio_file)
                except Exception as e:
                    print(f"Audio playback error: {e}")
                finally:
                    self.audio_queue.task_done()
        threading.Thread(target=audio_worker, daemon=True).start()

    # --- REFACTORED AI FUNCTIONS START HERE ---

    def load_model(self):
        """Load the GGUF-quantized Phi-3 model using llama-cpp-python."""
        try:
            self.status_var.set("Loading GGUF AI model... Please wait...")
            self.root.update_idletasks()
            
            model_repo = "second-state/Phi-3-mini-4k-instruct-GGUF"
            model_filename = "Phi-3-mini-4k-instruct-Q4_0.gguf"

            self.status_var.set(f"Downloading {model_filename} from {model_repo}...")
            self.root.update_idletasks()
            model_path = hf_hub_download(repo_id=model_repo, filename=model_filename)
            self.status_var.set("Download complete. Loading model to GPU...")
            self.root.update_idletasks()

            # n_gpu_layers=-1 attempts to offload all layers to the GPU.
            # This is the key for GPU acceleration.
            self.model = Llama(
                model_path=model_path,
                n_gpu_layers=25, 
                n_ctx=4096,
                verbose=False
            )
            
            self.model_loaded = True
            self.status_var.set("GGUF AI model loaded successfully! Ready to assist.")
        except Exception as e:
            error_message = f"Failed to load AI model: {str(e)}"
            self.status_var.set("Error: Model failed to load. Please restart.")
            messagebox.showerror("Critical Error", error_message)

    def construct_prompt(self, user_query):
        """Construct the chat prompt for the Llama.cpp model."""
        if self.current_language == "English":
            system_message = """You are an AI Health Encyclopedia. Your goal is to provide a comprehensive, structured overview of any health condition. Your response must be factual, informative, and strictly follow this format:

1. Disease Name: [Name of the disease or condition]

2. Disclaimer: DISCLAIMER: I am an AI assistant, not a medical professional. This information is for general knowledge only. Please consult a qualified doctor for any health concerns.

3. Overview: [A detailed but easy-to-understand explanation.]

4. Common Symptoms:
- [List of symptoms]

5. Common Treatments:
- [List of treatments]

6. General Home Remedies & Management:
- [List safe, non-prescriptive home care tips.]

7. When to Consult a Doctor: [Provide clear signs for seeking professional medical help.]"""
        else: # Marathi
            system_message = """You are an AI Health Encyclopedia. Your goal is to provide a comprehensive, structured overview of any health condition IN MARATHI. Your response must be factual, informative, in MARATHI, and strictly follow this format:

१. रोगाचे नाव: [Name of the disease or condition in Marathi]

२. अस्वीकरण: अस्वीकरण: मी एक AI सहाय्यक आहे, वैद्यकीय व्यावसायिक नाही. ही माहिती केवळ सामान्य ज्ञानासाठी आहे. कृपया कोणत्याही आरोग्यविषयक समस्यांसाठी पात्र डॉक्टरांचा सल्ला घ्या.

३. सर्वसाधारण माहिती: [A detailed but easy-to-understand explanation of the condition in Marathi.]

४. सामान्य लक्षणे:
- [List of symptoms in Marathi]

५. सामान्य उपचार:
- [List of treatments in Marathi]

६. सामान्य घरगुती उपाय आणि व्यवस्थापन:
- [List safe, non-prescriptive home care tips in Marathi.]

७. डॉक्टरांना कधी भेटावे: [Provide clear signs for seeking medical help in Marathi.]"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ]
        return messages

    def generate_response(self, prompt_messages):
        """Generate response using the Llama.cpp model."""
        try:
            response_object = self.model.create_chat_completion(
                messages=prompt_messages,
                temperature=0.7,
                max_tokens=1024 
            )
            response = response_object['choices'][0]['message']['content']
            return response.strip()
        except Exception as e:
            raise Exception(f"Model inference error: {str(e)}")

    def parse_response(self, response):
        """This function primarily ensures the response is not empty."""
        response = response.strip()
        if not response:
            if self.current_language == "English":
                return "I'm sorry, I couldn't generate a specific response for that topic. Could you please try rephrasing your question?"
            else:
                return "माफ करा, मी त्या विषयासाठी विशिष्ट प्रतिसाद तयार करू शकलो नाही. तुम्ही कृपया तुमचा प्रश्न पुन्हा मांडण्याचा प्रयत्न करू शकाल का?"
        return response

    # --- UNCHANGED FUNCTIONS START HERE ---

    def on_language_change(self, event=None):
        self.current_language = self.lang_var.get()
        self.add_message("System", f"Language changed to {self.current_language}", "system")
    
    def add_message(self, sender, message, msg_type="user"):
        timestamp = datetime.now().strftime("%H:%M")
        prefix = f"[{timestamp}]"
        if msg_type == "user":
            formatted_message = f"{prefix} You: {message}\n\n"
        elif msg_type == "assistant":
            formatted_message = f"{prefix} AI Assistant:\n{message}\n\n"
        else: # system
            formatted_message = f"{prefix} {message}\n\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        self.root.update_idletasks()
    
    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message: return
        self.input_field.delete(0, tk.END)
        self.add_message("You", message, "user")
        threading.Thread(target=self.process_message, args=(message, False), daemon=True).start()
    
    def start_speech_recognition(self):
        if self.is_listening: return
        self.is_listening = True
        self.speak_button.config(text="🔴 Listening...", bg='#e67e22')
        self.status_var.set("Listening... Please speak now!")
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def listen_for_speech(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            language = "en-IN" if self.current_language == "English" else "mr-IN"
            text = self.recognizer.recognize_google(audio, language=language)
            self.root.after(0, lambda: self.handle_speech_result(text))
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            self.root.after(0, lambda: self.handle_speech_result(""))
        except Exception as e:
            print(f"Speech recognition error: {e}")
            self.root.after(0, lambda: self.handle_speech_result(""))
        finally:
            self.root.after(0, self.reset_speech_ui)
    
    def handle_speech_result(self, text):
        if text:
            self.add_message("You", f"You said: {text}", "user")
            threading.Thread(target=self.process_message, args=(text, True), daemon=True).start()
        else:
            self.add_message("System", "Could not understand speech. Please try again.", "system")
    
    def reset_speech_ui(self):
        self.is_listening = False
        self.speak_button.config(text="🎤 Speak", bg='#e74c3c')
        self.status_var.set("Ready")
    
    def process_message(self, message, was_speech):
        if not self.model_loaded:
            self.root.after(0, lambda: self.add_message("System", "AI model is still loading. Please wait...", "system"))
            return
        
        try:
            self.status_var.set("AI is thinking...")
            prompt = self.construct_prompt(message)
            response = self.generate_response(prompt)
            formatted_response = self.parse_response(response)
            self.root.after(0, lambda: self.add_message("AI Assistant", formatted_response, "assistant"))
            if was_speech:
                self.root.after(0, lambda: self.generate_audio_response(formatted_response))
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, lambda: self.add_message("System", error_msg, "system"))
        finally:
             self.root.after(0, self.reset_speech_ui)

    def generate_audio_response(self, text_response):
        try:
            lines = text_response.split('\n')
            audio_text = " ".join(line.strip() for line in lines if line.strip() and not line.startswith('**') and not line.startswith('-'))
            if not audio_text: return
            
            language = "en" if self.current_language == "English" else "mr"
            tts = gTTS(text=audio_text, lang=language, slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                self.audio_queue.put(tmp_file.name)
        except Exception as e:
            print(f"Audio generation error: {e}")

def main():
    root = tk.Tk()
    app = HealthAssistantApp(root)
    
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.audio_queue.put(None)
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()