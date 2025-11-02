from ddgs import DDGS
import ollama
import time
import json
import os
import asyncio
try:
    import pygame
except ImportError:
    import pygame_ce as pygame
from datetime import datetime
try:
    import edge_tts
except ImportError:
    edge_tts = None

class DefaultAISystem:
    def __init__(self):
        print("🤖 Initializing ΛI-NEXUS AI System...")
        
        # Auto-cleanup
        self.auto_cleanup()
        
        # Initialize all variables first
        self.error_count = 0
        self.max_errors = 3
        self.last_heal_time = time.time()
        self.health_status = "healthy"
        self.conversation_history = []
        self.learning_score = 0
        self.edge_available = False
        
        # Load settings and knowledge base
        self.settings = self.load_default_settings()
        self.knowledge_base = self.load_knowledge_base()
        
        # Setup components
        self.setup_edge_tts()
        self.model = self.get_model()
        
        print(f"✅ ΛI-NEXUS Ready - Model: {self.model}")
    
    def load_knowledge_base(self):
        try:
            if os.path.exists('ai_knowledge_base.json'):
                with open('ai_knowledge_base.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'fed_data': [],
            'learned_concepts': {},
            'reinforcement_scores': {},
            'last_update': datetime.now().isoformat()
        }
    
    def save_knowledge_base(self):
        try:
            self.knowledge_base['last_update'] = datetime.now().isoformat()
            with open('ai_knowledge_base.json', 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            print(f"Knowledge save error: {e}")
    
    def load_default_settings(self):
        default_settings = {
            "ai_model": "phi3:mini",
            "voice": "en-US-AriaNeural",
            "speech_enabled": True,
            "search_enabled": True,
            "response_length": 150,
            "temperature": 0.7,
            "ai_name": "ΛI-NEXUS",
            "auto_reset": False
        }
        
        try:
            if os.path.exists('ai_settings.json'):
                with open('ai_settings.json', 'r') as f:
                    settings = json.load(f)
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except:
            pass
        
        self.save_settings(default_settings)
        return default_settings
    
    def save_settings(self, settings=None):
        try:
            if settings is None:
                settings = self.settings
            with open('ai_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
        except:
            pass
    
    def setup_edge_tts(self):
        self.edge_available = False
        
        if not self.settings["speech_enabled"]:
            return
        
        if edge_tts is None:
            print("❌ Edge TTS not installed")
            return
        
        try:
            self.voice = self.settings["voice"]
            print(f"🔊 Edge TTS ready - Voice: {self.voice}")
            self.edge_available = True
        except Exception as e:
            print(f"❌ TTS error: {e}")
            self.edge_available = False
    
    def speak_edge(self, text):
        if not self.edge_available:
            return
        
        try:
            print("🗣️ Speaking...")
            asyncio.run(self._generate_speech(text))
            print("✅ Speech done")
        except Exception as e:
            print(f"Speech error: {e}")
    
    async def _generate_speech(self, text):
        clean_text = text.replace('\n', ' ').replace('\r', ' ').strip()
        if not clean_text:
            return
            
        communicate = edge_tts.Communicate(clean_text, self.voice)
        temp_file = f"temp_speech_{int(time.time())}.mp3"
        
        try:
            await communicate.save(temp_file)
            
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
            except:
                import sys
                if sys.platform == "win32":
                    os.startfile(temp_file)
                    await asyncio.sleep(3)
                
        finally:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except:
                pass
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def get_model(self):
        try:
            model = self.settings["ai_model"]
            ollama.generate(model=model, prompt='test', options={'num_predict': 1})
            return model
        except:
            for model in ['phi3:mini', 'gemma:2b', 'llama2:latest']:
                try:
                    ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                    self.settings["ai_model"] = model
                    return model
                except:
                    continue
            return 'phi3:mini'
    
    def search_web(self, query):
        if not self.settings["search_enabled"]:
            return []
        
        try:
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=3)):
                    if i >= 3:
                        break
                    results.append({
                        'title': result['title'],
                        'content': result['body'][:300]
                    })
                if results:
                    print(f"🔍 Found {len(results)} results")
                return results
        except:
            return []
    
    def should_search(self, user_input):
        search_triggers = [
            'news', 'latest', 'current', 'today', 'happening', 'recent',
            'what is', 'who is', 'when', 'where', 'how', 'why',
            'information', 'update', 'story', 'events'
        ]
        
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in search_triggers)
    
    def use_fed_knowledge(self, query):
        relevant_knowledge = []
        
        if any(word in query.lower() for word in ['shaik', 'davood', 'creator', 'who created', 'who made', 'who is']):
            for entry in self.knowledge_base['fed_data']:
                if any(word in entry['content'].lower() for word in ['shaik', 'davood', 'mechanical', 'engineering', 'nbkr']):
                    relevant_knowledge.append(entry)
                    entry['usage_count'] = entry.get('usage_count', 0) + 1
                    entry['reinforcement_score'] = entry.get('reinforcement_score', 1.0) + 0.2
        
        return relevant_knowledge[:2]
    
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
        
        return f"System optimized! Cleaned {removed} files for smoother performance."
    
    def generate_response(self, user_input, search_results=None):
        try:
            context = f"You are Lambda I-NEXUS, an AI assistant. Answer questions directly and naturally. Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            fed_knowledge = self.use_fed_knowledge(user_input)
            if fed_knowledge and any(word in user_input.lower() for word in ['who', 'creator', 'made', 'davood']):
                context += "CREATOR INFO:\n"
                for i, knowledge in enumerate(fed_knowledge, 1):
                    context += f"{i}. {knowledge['content'][:200]}\n"
            
            if search_results:
                context += "SEARCH RESULTS:\n"
                for i, result in enumerate(search_results, 1):
                    context += f"{i}. {result['title']}: {result['content'][:300]}\n"
            
            if self.conversation_history:
                context += "Recent conversation:\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\n"
            
            prompt = f"{context}User: {user_input}\nΛI-NEXUS:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': self.settings["response_length"],
                    'temperature': self.settings["temperature"]
                }
            )
            
            result = response['response'].strip()
            if not result:
                result = "I'm ΛI-NEXUS, your AI assistant. How can I help you?"
            return result
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def run(self):
        print("\n" + "="*60)
        print("🤖 ΛI-NEXUS - REVOLUTIONARY AI SYSTEM")
        print("Features: Neural Voice, AI Auto-Search, Data Feeding")
        print("="*60)
        
        welcome = "Hello! I'm ΛI-NEXUS, your AI assistant. How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak_edge(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Your settings are saved."
                    print(f"AI: {goodbye}")
                    self.speak_edge(goodbye)
                    break
                
                elif user_input.lower() in ['cleanup', 'clean', 'optimize']:
                    cleanup_msg = self.smart_cleanup()
                    print(f"AI: {cleanup_msg}")
                    self.speak_edge(cleanup_msg)
                    continue
                
                if user_input:
                    start_time = time.time()
                    
                    self.conversation_history.append(f"User: {user_input}")
                    
                    search_results = []
                    if self.should_search(user_input):
                        print("🤖 AI decided to search for information...")
                        search_results = self.search_web(user_input)
                    
                    response = self.generate_response(user_input, search_results)
                    
                    self.conversation_history.append(f"AI: {response}")
                    
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    response_time = time.time() - start_time
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                    
                    self.speak_edge(response)
                    self.save_settings()
                
            except KeyboardInterrupt:
                print("\n👋 AI System shutting down...")
                break
            except Exception as e:
                print(f"System error: {e}")

if __name__ == "__main__":
    ai = DefaultAISystem()
    ai.run()