try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
import asyncio
import pygame
from datetime import datetime
try:
    import edge_tts
except ImportError:
    edge_tts = None

class AIWithEdgeTTS:
    def __init__(self):
        print("🤖 Initializing AI with Edge Neural TTS...")
        
        # Setup Edge TTS
        self.setup_edge_tts()
        
        # AI settings
        self.model = self.get_model()
        self.conversation_history = []
        
        print(f"✅ AI System Ready - Model: {self.model}")
    
    def setup_edge_tts(self):
        """Setup Edge neural TTS"""
        self.edge_available = False
        
        if edge_tts is None:
            print("❌ Edge TTS not installed")
            print("Run: pip install edge-tts pygame")
            return
        
        try:
            # Test Edge TTS
            self.voice = "en-US-AriaNeural"  # High quality female voice
            print(f"🔊 Edge neural TTS ready - Voice: {self.voice}")
            self.edge_available = True
            
        except Exception as e:
            print(f"❌ Edge TTS setup error: {e}")
    
    def speak_edge(self, text):
        """Speak using Edge neural TTS"""
        if not self.edge_available:
            print("(Neural speech not available)")
            return
        
        try:
            print("🗣️ Speaking with neural voice...")
            
            # Generate speech
            asyncio.run(self._generate_speech(text))
            
            print("✅ Neural speech completed")
            
        except Exception as e:
            print(f"Edge speech error: {e}")
    
    async def _generate_speech(self, text):
        """Generate speech with Edge TTS"""
        communicate = edge_tts.Communicate(text, self.voice)
        
        # Save to file
        temp_file = "temp_speech.mp3"
        await communicate.save(temp_file)
        
        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for playback
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        # Cleanup
        pygame.mixer.quit()
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    def get_model(self):
        """Get working AI model"""
        models = ['phi3:mini', 'gemma:2b', 'llama2:latest']
        for model in models:
            try:
                ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                return model
            except:
                continue
        return 'phi3:mini'
    
    def search_web(self, query):
        """Search web for information"""
        try:
            print(f"🔍 Searching: {query}")
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=3)):
                    if i >= 3:
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
        """Generate AI response"""
        try:
            context = f"Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            if search_results:
                context += "Search information:\n"
                for result in search_results:
                    context += f"- {result['title']}: {result['content'][:200]}...\n"
                context += "\n"
            
            if self.conversation_history:
                context += "Recent conversation:\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\n"
                context += "\n"
            
            prompt = f"{context}User: {user_input}\nAI:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': 150,
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            )
            
            return response['response'].strip()
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def run(self):
        """Main AI system loop"""
        print("\n" + "="*60)
        print("🤖 AI SYSTEM WITH EDGE NEURAL TTS")
        print("Features: Chat, Web Search, Human-like Voice")
        print("="*60)
        
        welcome = "Hello! I'm ΛI-NEXUS, your AI assistant with Edge neural text-to-speech. My voice should sound very natural and human-like. How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak_edge(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Thank you for trying the Edge neural voice AI system!"
                    print(f"AI: {goodbye}")
                    self.speak_edge(goodbye)
                    break
                
                if user_input:
                    start_time = time.time()
                    
                    # Add to conversation history
                    self.conversation_history.append(f"User: {user_input}")
                    
                    # Check if search needed
                    search_keywords = ['search', 'find', 'what is', 'who is', 'latest', 'news', 'current', 'today']
                    needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
                    
                    # Search if needed
                    search_results = []
                    if needs_search:
                        search_results = self.search_web(user_input)
                    
                    # Generate response
                    response = self.generate_response(user_input, search_results)
                    
                    # Add to conversation history
                    self.conversation_history.append(f"AI: {response}")
                    
                    # Keep history manageable
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    # Show response
                    response_time = time.time() - start_time
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                    
                    # Speak with neural voice
                    self.speak_edge(response)
                
            except KeyboardInterrupt:
                print("\n👋 AI System shutting down...")
                break
            except Exception as e:
                error_msg = "I'm sorry, I encountered an error. Please try again."
                print(f"AI: {error_msg}")
                self.speak_edge(error_msg)

if __name__ == "__main__":
    ai = AIWithEdgeTTS()
    ai.run()