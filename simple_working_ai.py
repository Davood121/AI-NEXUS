import pyttsx3
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
from datetime import datetime

class SimpleWorkingAI:
    def __init__(self):
        print("Starting Simple AI System...")
        
        # Initialize voice
        self.setup_voice()
        
        # Get model
        self.model = self.get_working_model()
        
        # Simple backup
        self.backup_file = "ai_backup.json"
        
        print(f"AI Ready - Model: {self.model}")
        print(f"Voice: {'Working' if self.voice_ok else 'Disabled'}")
    
    def setup_voice(self):
        """Simple voice setup"""
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 200)
            
            # Test voice
            self.tts.say("Test")
            self.tts.runAndWait()
            
            self.voice_ok = True
            print("Voice: OK")
        except Exception as e:
            print(f"Voice failed: {e}")
            self.voice_ok = False
    
    def get_working_model(self):
        """Get a working model"""
        models = ['phi3:mini', 'gemma:2b', 'llama2:latest']
        
        for model in models:
            try:
                print(f"Testing {model}...")
                result = ollama.generate(
                    model=model, 
                    prompt='Hi', 
                    options={'num_predict': 5}
                )
                print(f"✅ {model} works!")
                return model
            except Exception as e:
                print(f"❌ {model} failed: {e}")
        
        print("⚠️ No models working - using phi3:mini anyway")
        return 'phi3:mini'
    
    def speak(self, text):
        """Simple speech"""
        if not self.voice_ok:
            return
        
        try:
            print("🗣️ Speaking...")
            self.tts.say(text)
            self.tts.runAndWait()
            print("✅ Done speaking")
        except Exception as e:
            print(f"Speech error: {e}")
            self.voice_ok = False
    
    def search_info(self, query):
        """Simple search"""
        try:
            print(f"🔍 Searching: {query}")
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=2)):
                    if i >= 2:
                        break
                    results.append(result['body'][:200])
                
                if results:
                    print(f"✅ Found {len(results)} results")
                    return ' '.join(results)
                else:
                    print("❌ No results found")
                    return ""
        except Exception as e:
            print(f"Search error: {e}")
            return ""
    
    def get_response(self, user_input):
        """Get AI response"""
        try:
            print("🤔 Thinking...")
            
            # Check if search needed
            search_words = ['search', 'find', 'what is', 'news', 'current', 'latest', 'today']
            needs_search = any(word in user_input.lower() for word in search_words)
            
            # Build prompt
            if needs_search:
                search_info = self.search_info(user_input)
                if search_info:
                    prompt = f"Information: {search_info}\n\nUser: {user_input}\nAI:"
                else:
                    prompt = f"User: {user_input}\nAI:"
            else:
                prompt = f"User: {user_input}\nAI:"
            
            # Generate response
            print("🧠 Generating response...")
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': 150,
                    'temperature': 0.7
                }
            )
            
            result = response['response'].strip()
            print("✅ Response generated")
            return result
            
        except Exception as e:
            error_msg = f"Sorry, I had an error: {str(e)}"
            print(f"❌ Error: {e}")
            return error_msg
    
    def backup_conversation(self, user_input, ai_response):
        """Simple backup"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'user': user_input,
                'ai': ai_response
            }
            
            # Load existing backups
            backups = []
            if os.path.exists(self.backup_file):
                try:
                    with open(self.backup_file, 'r') as f:
                        backups = json.load(f)
                except:
                    backups = []
            
            # Add new backup
            backups.append(backup_data)
            
            # Keep only last 50 conversations
            if len(backups) > 50:
                backups = backups[-50:]
            
            # Save backups
            with open(self.backup_file, 'w') as f:
                json.dump(backups, f, indent=2)
            
            print("💾 Conversation backed up")
            
        except Exception as e:
            print(f"Backup error: {e}")
    
    def run(self):
        """Main loop"""
        print("\n" + "="*50)
        print("🤖 SIMPLE WORKING AI SYSTEM")
        print("Features: Chat, Search, Voice, Auto-backup")
        print("="*50)
        
        # Welcome
        welcome = "Hello! I'm ΛI-NEXUS, your AI assistant. I can chat, search the web, and speak responses. How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Thanks for chatting with me!"
                    print(f"AI: {goodbye}")
                    self.speak(goodbye)
                    break
                
                if user_input:
                    # Get response
                    start_time = time.time()
                    response = self.get_response(user_input)
                    response_time = time.time() - start_time
                    
                    # Show response
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                    
                    # Speak response
                    self.speak(response)
                    
                    # Backup conversation
                    self.backup_conversation(user_input, response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"System error: {e}")
                error_msg = "I encountered a system error. Please try again."
                print(f"AI: {error_msg}")
                self.speak(error_msg)

if __name__ == "__main__":
    ai = SimpleWorkingAI()
    ai.run()