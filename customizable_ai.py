try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
from datetime import datetime
import pyttsx3

class CustomizableAI:
    def __init__(self):
        print("🤖 Initializing Customizable AI System...")
        
        # Auto-cleanup
        self.auto_cleanup()
        
        # Load or create settings
        self.settings = self.load_settings()
        
        # Setup components based on settings
        self.setup_tts()
        self.setup_ai()
        
        print(f"✅ AI Ready with custom settings!")
    
    def load_settings(self):
        """Load settings from file or create defaults"""
        try:
            if os.path.exists('ai_settings.json'):
                with open('ai_settings.json', 'r') as f:
                    settings = json.load(f)
                    print("📋 Loaded custom settings")
                    return settings
        except:
            pass
        
        # Default settings
        default_settings = {
            "ai_model": "phi3:mini",
            "speech_enabled": True,
            "speech_rate": 180,
            "speech_volume": 1.0,
            "voice_index": 0,
            "response_length": 150,
            "temperature": 0.7,
            "search_enabled": True,
            "max_search_results": 3,
            "conversation_memory": 10,
            "ai_name": "ΛI-NEXUS",
            "personality": "helpful and friendly",
            "auto_save": True
        }
        
        self.save_settings(default_settings)
        print("📋 Created default settings")
        return default_settings
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        try:
            if settings is None:
                settings = self.settings
            with open('ai_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Settings save error: {e}")
    
    def setup_tts(self):
        """Setup TTS based on settings"""
        self.tts_available = False
        
        if not self.settings["speech_enabled"]:
            print("🔇 Speech disabled in settings")
            return
        
        try:
            self.tts = pyttsx3.init()
            
            # Apply speech settings
            self.tts.setProperty('rate', self.settings["speech_rate"])
            self.tts.setProperty('volume', self.settings["speech_volume"])
            
            # Set voice
            voices = self.tts.getProperty('voices')
            if voices and len(voices) > self.settings["voice_index"]:
                self.tts.setProperty('voice', voices[self.settings["voice_index"]].id)
                print(f"🔊 Voice: {voices[self.settings['voice_index']].name}")
            
            self.tts_available = True
            print(f"🔊 TTS ready - Rate: {self.settings['speech_rate']}, Volume: {self.settings['speech_volume']}")
            
        except Exception as e:
            print(f"TTS setup error: {e}")
    
    def setup_ai(self):
        """Setup AI based on settings"""
        self.model = self.settings["ai_model"]
        self.conversation_history = []
        
        # Test model
        try:
            ollama.generate(model=self.model, prompt='test', options={'num_predict': 1})
            print(f"🧠 AI Model: {self.model}")
        except:
            print(f"⚠️ Model {self.model} not available, trying alternatives...")
            for alt_model in ['phi3:mini', 'gemma:2b', 'llama2:latest']:
                try:
                    ollama.generate(model=alt_model, prompt='test', options={'num_predict': 1})
                    self.model = alt_model
                    self.settings["ai_model"] = alt_model
                    print(f"🧠 Using alternative model: {alt_model}")
                    break
                except:
                    continue
    
    def speak(self, text):
        """Speak text based on settings"""
        if not self.tts_available:
            return
        
        try:
            print("🗣️ Speaking...")
            self.tts.say(text)
            self.tts.runAndWait()
            print("✅ Speech done")
        except Exception as e:
            print(f"Speech error: {e}")
    
    def search_web(self, query):
        """Search web based on settings"""
        if not self.settings["search_enabled"]:
            print("🔍 Search disabled in settings")
            return []
        
        try:
            print(f"🔍 Searching: {query}")
            with DDGS() as ddgs:
                results = []
                max_results = self.settings["max_search_results"]
                
                for i, result in enumerate(ddgs.text(query, max_results=max_results)):
                    if i >= max_results:
                        break
                    results.append({
                        'title': result['title'],
                        'content': result['body'][:300]
                    })
                
                print(f"✅ Found {len(results)} results")
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def generate_response(self, user_input, search_results=None):
        """Generate AI response based on settings"""
        try:
            # Build context with personality
            context = f"I am {self.settings['ai_name']}, an AI assistant who is {self.settings['personality']}.\n"
            context += f"Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            if search_results:
                context += "Search information:\n"
                for result in search_results:
                    context += f"- {result['title']}: {result['content'][:200]}...\n"
                context += "\n"
            
            # Add conversation memory based on settings
            memory_limit = self.settings["conversation_memory"]
            if self.conversation_history and memory_limit > 0:
                context += "Recent conversation:\n"
                for msg in self.conversation_history[-memory_limit:]:
                    context += f"{msg}\n"
                context += "\n"
            
            prompt = f"{context}User: {user_input}\nAI:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': self.settings["response_length"],
                    'temperature': self.settings["temperature"],
                    'top_p': 0.9
                }
            )
            
            return response['response'].strip()
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def show_settings(self):
        """Display current settings"""
        print("\n" + "="*50)
        print("⚙️ CURRENT AI SETTINGS")
        print("="*50)
        for key, value in self.settings.items():
            print(f"{key}: {value}")
        print("="*50)
    
    def auto_cleanup(self):
        """Auto cleanup on startup"""
        cleaned = 0
        try:
            for file in os.listdir('.'):
                if file.startswith('temp_speech_') and file.endswith('.mp3'):
                    try:
                        os.remove(file)
                        cleaned += 1
                    except:
                        pass
        except:
            pass
        
        if cleaned > 0:
            print(f"🧹 Auto-cleaned {cleaned} temporary files")
    
    def smart_cleanup(self):
        """Smart cleanup function"""
        unwanted_files = ['temp_speech.mp3', 'test_edge_neural.mp3']
        removed = 0
        
        for file in unwanted_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    removed += 1
                except:
                    pass
        
        try:
            for file in os.listdir('.'):
                if (file.startswith('temp_speech_') and file.endswith('.mp3') or
                    file.endswith('.tmp') or file.endswith('.log')):
                    try:
                        os.remove(file)
                        removed += 1
                    except:
                        pass
        except:
            pass
        
        return f"System optimized! Cleaned {removed} files for better performance."
    
    def change_settings(self):
        """Interactive settings change"""
        print("\n🔧 CHANGE AI SETTINGS")
        print("="*30)
        
        # Show current settings
        for i, (key, value) in enumerate(self.settings.items(), 1):
            print(f"{i}. {key}: {value}")
        
        try:
            choice = input("\nEnter setting number to change (or 'done'): ").strip()
            
            if choice.lower() == 'done':
                return
            
            choice_num = int(choice) - 1
            setting_keys = list(self.settings.keys())
            
            if 0 <= choice_num < len(setting_keys):
                key = setting_keys[choice_num]
                current_value = self.settings[key]
                
                print(f"\nChanging '{key}' (current: {current_value})")
                
                if isinstance(current_value, bool):
                    new_value = input("Enter true/false: ").strip().lower() == 'true'
                elif isinstance(current_value, int):
                    new_value = int(input("Enter number: ").strip())
                elif isinstance(current_value, float):
                    new_value = float(input("Enter decimal: ").strip())
                else:
                    new_value = input("Enter new value: ").strip()
                
                self.settings[key] = new_value
                self.save_settings()
                
                print(f"✅ Changed '{key}' to: {new_value}")
                print("🔄 Restart AI to apply all changes")
            
        except Exception as e:
            print(f"Settings change error: {e}")
    
    def run(self):
        """Main AI loop"""
        print("\n" + "="*60)
        print(f"🤖 {self.settings['ai_name'].upper()} - CUSTOMIZABLE AI SYSTEM")
        print("Features: Fully Customizable Settings")
        print("="*60)
        
        welcome = f"Hello! I'm ΛI-NEXUS, your customizable AI assistant. Type 'settings' to change my configuration. How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Your settings have been saved."
                    print(f"AI: {goodbye}")
                    self.speak(goodbye)
                    break
                
                elif user_input.lower() == 'settings':
                    self.show_settings()
                    self.change_settings()
                    continue
                
                elif user_input.lower() == 'show settings':
                    self.show_settings()
                    continue
                
                elif user_input.lower() in ['cleanup', 'clean', 'optimize']:
                    cleanup_msg = self.smart_cleanup()
                    print(f"AI: {cleanup_msg}")
                    self.speak(cleanup_msg)
                    continue
                
                if user_input:
                    # Add to conversation history
                    if self.settings["conversation_memory"] > 0:
                        self.conversation_history.append(f"User: {user_input}")
                    
                    # Check if search needed
                    search_keywords = ['search', 'find', 'what is', 'who is', 'latest', 'news', 'current', 'today', 'recent']
                    needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
                    
                    # Search if needed and enabled
                    search_results = []
                    if needs_search:
                        search_results = self.search_web(user_input)
                    
                    # Generate response
                    start_time = time.time()
                    response = self.generate_response(user_input, search_results)
                    response_time = time.time() - start_time
                    
                    # Add to conversation history
                    if self.settings["conversation_memory"] > 0:
                        self.conversation_history.append(f"AI: {response}")
                        
                        # Keep history within limit
                        memory_limit = self.settings["conversation_memory"] * 2  # User + AI pairs
                        if len(self.conversation_history) > memory_limit:
                            self.conversation_history = self.conversation_history[-memory_limit:]
                    
                    # Show response
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                    
                    # Speak if enabled
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                error_msg = "Sorry, I encountered an error."
                print(f"AI: {error_msg}")
                self.speak(error_msg)

if __name__ == "__main__":
    ai = CustomizableAI()
    ai.run()