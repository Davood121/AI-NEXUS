try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
import wave
import pygame
from datetime import datetime
try:
    from piper import PiperVoice
except ImportError:
    PiperVoice = None

class AIWithPiperTTS:
    def __init__(self):
        print("🤖 Initializing AI with Piper Neural TTS...")
        
        # Setup Piper TTS
        self.setup_piper_tts()
        
        # AI settings
        self.model = self.get_model()
        self.conversation_history = []
        
        print(f"✅ AI System Ready - Model: {self.model}")
    
    def setup_piper_tts(self):
        """Setup Piper neural TTS"""
        self.piper_available = False
        self.model_path = "piper_voice_models/en_US-amy-medium.onnx"
        
        if PiperVoice is None:
            print("❌ Piper TTS not installed")
            print("Run: pip install piper-tts")
            return
        
        try:
            if os.path.exists(self.model_path):
                self.voice = PiperVoice.load(self.model_path)
                print("🔊 Piper neural TTS ready with Amy voice")
                self.piper_available = True
            else:
                print("❌ Piper voice model not found")
                print("Run: python setup_piper.py to download voice model")
                
        except Exception as e:
            print(f"❌ Piper setup error: {e}")
    
    def speak_piper(self, text):
        """Speak using Piper neural TTS"""
        if not self.piper_available:
            print("(Neural speech not available)")
            return
        
        try:
            print("🗣️ Speaking with neural voice...")
            
            # Generate audio data
            audio_data = b''
            for audio_chunk in self.voice.synthesize(text):
                audio_data += audio_chunk
            
            # Save to temporary WAV file
            temp_wav = "temp_speech.wav"
            with wave.open(temp_wav, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(22050)
                wav_file.writeframes(audio_data)
            
            # Play the audio
            pygame.mixer.init(frequency=22050)
            pygame.mixer.music.load(temp_wav)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Cleanup
            pygame.mixer.quit()
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            
            print("✅ Neural speech completed")
            
        except Exception as e:
            print(f"Piper speech error: {e}")
    
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
        print("🤖 AI SYSTEM WITH PIPER NEURAL TTS")
        print("Features: Chat, Web Search, Human-like Voice")
        print("="*60)
        
        welcome = "Hello! I'm ΛI-NEXUS, your AI assistant with neural text-to-speech. My voice should sound much more human-like. How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak_piper(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Thank you for trying the neural voice AI system!"
                    print(f"AI: {goodbye}")
                    self.speak_piper(goodbye)
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
                    self.speak_piper(response)
                
            except KeyboardInterrupt:
                print("\n👋 AI System shutting down...")
                break
            except Exception as e:
                error_msg = "I'm sorry, I encountered an error. Please try again."
                print(f"AI: {error_msg}")
                self.speak_piper(error_msg)

if __name__ == "__main__":
    ai = AIWithPiperTTS()
    ai.run()