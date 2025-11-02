from ddgs import DDGS
import ollama
import time
import json
import os
import asyncio
import sys
from datetime import datetime

try:
    import pygame
except ImportError:
    try:
        import pygame_ce as pygame
    except ImportError:
        pygame = None

try:
    import edge_tts
except ImportError:
    edge_tts = None

class StableAI:
    def __init__(self):
        print("🤖 Initializing Stable AI System...")
        
        # Auto-cleanup on startup
        self.auto_cleanup()
        
        # Core variables
        self.conversation_history = []
        self.edge_available = False
        self.model = None
        
        # Load settings with error handling
        self.settings = self.safe_load_settings()
        
        # Initialize components safely
        self.safe_setup_tts()
        self.safe_setup_model()
        
        print(f"✅ Stable AI Ready - Model: {self.model}")
    
    def safe_load_settings(self):
        """Load settings with full error protection"""
        default = {
            "ai_model": "phi3:mini",
            "voice": "en-US-AriaNeural",
            "speech_enabled": True,
            "search_enabled": True,
            "response_length": 150,
            "temperature": 0.7
        }
        
        try:
            if os.path.exists('ai_settings.json'):
                with open('ai_settings.json', 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    for key, value in default.items():
                        if key not in loaded:
                            loaded[key] = value
                    return loaded
        except:
            pass
        
        # Save defaults
        try:
            with open('ai_settings.json', 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=2)
        except:
            pass
        
        return default
    
    def safe_setup_tts(self):
        """Setup TTS with error protection"""
        self.edge_available = False
        
        if not self.settings.get("speech_enabled", False):
            return
        
        if edge_tts is None:
            return
        
        try:
            self.voice = self.settings.get("voice", "en-US-AriaNeural")
            self.edge_available = True
            print(f"🔊 TTS Ready - Voice: {self.voice}")
        except:
            self.edge_available = False
    
    def safe_setup_model(self):
        """Setup AI model with fallbacks"""
        models_to_try = [
            self.settings.get("ai_model", "phi3:mini"),
            "phi3:mini",
            "gemma:2b", 
            "llama2:latest"
        ]
        
        for model in models_to_try:
            try:
                ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                self.model = model
                return
            except:
                continue
        
        self.model = "phi3:mini"  # Fallback
    
    def safe_speak(self, text):
        """Safe speech with error handling"""
        if not self.edge_available or not text:
            return
        
        try:
            asyncio.run(self._safe_generate_speech(text))
        except:
            pass  # Silent fail
    
    async def _safe_generate_speech(self, text):
        """Generate speech safely"""
        try:
            clean_text = text.replace('\n', ' ').strip()[:500]  # Limit length
            if not clean_text:
                return
            
            communicate = edge_tts.Communicate(clean_text, self.voice)
            temp_file = f"temp_speech_{int(time.time())}.mp3"
            
            await communicate.save(temp_file)
            
            # Try pygame first
            if pygame:
                try:
                    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)
                    
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                except:
                    # Fallback to system player
                    if sys.platform == "win32":
                        os.startfile(temp_file)
                        await asyncio.sleep(2)
            
            # Cleanup
            try:
                os.remove(temp_file)
            except:
                pass
                
        except:
            pass  # Silent fail
    
    def safe_search(self, query):
        """Safe web search with error handling"""
        if not self.settings.get("search_enabled", True):
            return []
        
        try:
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=3)):
                    if i >= 3:
                        break
                    results.append({
                        'title': result.get('title', ''),
                        'content': result.get('body', '')[:300]
                    })
                return results
        except:
            return []
    
    def should_search(self, user_input):
        """Determine if search is needed"""
        triggers = ['what is', 'who is', 'how', 'why', 'when', 'where', 'latest', 'news', 'current']
        return any(trigger in user_input.lower() for trigger in triggers)
    
    def safe_generate_response(self, user_input, search_results=None):
        """Generate response with error protection"""
        try:
            context = f"You are Lambda I-NEXUS, an AI assistant. Current time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            
            if search_results:
                context += "Search results:\n"
                for i, result in enumerate(search_results[:2], 1):
                    context += f"{i}. {result['title']}: {result['content'][:200]}\n"
            
            if self.conversation_history:
                context += "Recent chat:\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\n"
            
            prompt = f"{context}\nUser: {user_input}\nAI:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': self.settings.get("response_length", 150),
                    'temperature': self.settings.get("temperature", 0.7)
                }
            )
            
            result = response.get('response', '').strip()
            return result if result else "I'm here to help! What would you like to know?"
            
        except Exception as e:
            return f"I encountered an issue: {str(e)[:100]}"
    
    def auto_cleanup(self):
        """Automatic cleanup of unwanted files"""
        unwanted_patterns = [
            'temp_speech_*.mp3',
            '*.tmp',
            '*.log',
            '__pycache__',
            '*.pyc',
            '.DS_Store',
            'Thumbs.db'
        ]
        
        unwanted_files = [
            'temp_speech.mp3',
            'test_edge_neural.mp3'
        ]
        
        cleaned = 0
        
        # Remove specific unwanted files
        for file in unwanted_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    cleaned += 1
                except:
                    pass
        
        # Remove temp speech files
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
    
    def manual_cleanup(self):
        """Manual cleanup command"""
        print("🧹 Running manual cleanup...")
        
        # Files safe to remove
        cleanup_files = [
            'ai_with_edge_tts.py',
            'ai_with_offline_tts.py',
            'simple_ai.py',
            'simple_text_ai.py',
            'working_ai.py',
            'temp_speech.mp3',
            'test_edge_neural.mp3'
        ]
        
        removed = 0
        for file in cleanup_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    removed += 1
                    print(f"✅ Removed: {file}")
                except:
                    print(f"❌ Failed to remove: {file}")
        
        # Clean temp files
        try:
            for file in os.listdir('.'):
                if (file.startswith('temp_') or 
                    file.endswith('.tmp') or 
                    file.endswith('.log')):
                    try:
                        os.remove(file)
                        removed += 1
                    except:
                        pass
        except:
            pass
        
        print(f"🎉 Cleanup complete! Removed {removed} files")
        return f"Cleaned up {removed} unwanted files to optimize performance."
    
    def run(self):
        """Main stable AI loop"""
        print("\n" + "="*50)
        print("🤖 STABLE AI SYSTEM")
        print("="*50)
        
        welcome = "Hello! I'm your stable AI assistant. How can I help you?"
        print(f"\nAI: {welcome}")
        self.safe_speak(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye!"
                    print(f"AI: {goodbye}")
                    self.safe_speak(goodbye)
                    break
                
                elif user_input.lower() in ['cleanup', 'clean', 'optimize']:
                    response = self.manual_cleanup()
                    print(f"AI: {response}")
                    self.safe_speak(response)
                    continue
                
                if not user_input:
                    continue
                
                start_time = time.time()
                
                # Add to history
                self.conversation_history.append(f"User: {user_input}")
                
                # Search if needed
                search_results = []
                if self.should_search(user_input):
                    search_results = self.safe_search(user_input)
                    if search_results:
                        print(f"🔍 Found {len(search_results)} results")
                
                # Generate response
                response = self.safe_generate_response(user_input, search_results)
                
                # Add to history
                self.conversation_history.append(f"AI: {response}")
                
                # Keep history manageable
                if len(self.conversation_history) > 8:
                    self.conversation_history = self.conversation_history[-8:]
                
                # Show response
                response_time = time.time() - start_time
                print(f"[{response_time:.1f}s] AI: {response}")
                
                # Speak response
                self.safe_speak(response)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue  # Keep running

if __name__ == "__main__":
    ai = StableAI()
    ai.run()