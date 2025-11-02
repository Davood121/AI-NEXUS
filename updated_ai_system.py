import pyttsx3
from duckduckgo_search import DDGS
import ollama
import threading
import time
import os
from datetime import datetime

class UpdatedAISystem:
    def __init__(self):
        # Initialize TTS
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 200)
        self.tts.setProperty('volume', 1.0)
        self.tts_lock = threading.Lock()
        
        # Conversation memory
        self.conversation_history = []
        
        # Auto-detect best model
        self.model = self.detect_best_model()
        
        print(f"🤖 AI System Ready - Using: {self.model}")
        
    def detect_best_model(self):
        """Auto-detect fastest available model"""
        models_to_try = ['gemma:2b', 'phi3:mini', 'llama2:latest']
        
        for model in models_to_try:
            try:
                start_time = time.time()
                ollama.generate(model=model, prompt='Hi', options={'num_predict': 1})
                response_time = time.time() - start_time
                
                if response_time < 5:  # If fast enough
                    print(f"✅ Selected fast model: {model}")
                    return model
            except:
                continue
        
        print("⚠️ Using default model: phi3:mini")
        return 'phi3:mini'
    
    def speak_async(self, text):
        """Non-blocking speech"""
        def speak():
            with self.tts_lock:
                try:
                    self.tts.say(text)
                    self.tts.runAndWait()
                except:
                    pass
        threading.Thread(target=speak, daemon=True).start()
    
    def web_search(self, query, max_results=3):
        """Fast web search"""
        try:
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=max_results)):
                    if i >= max_results:
                        break
                    results.append({
                        'title': result['title'][:100],
                        'body': result['body'][:300]
                    })
                return results
        except:
            return []
    
    def generate_response(self, user_input, search_results=None):
        """Generate complete AI response"""
        try:
            # Build context
            context = ""
            if search_results:
                context = "Search info: "
                for result in search_results[:2]:
                    context += f"{result['body'][:200]} "
                context += "\n"
            
            # Simple prompt for better responses
            prompt = f"{context}User: {user_input}\nAI:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': -1,      # Complete responses
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'repeat_penalty': 1.1,
                    'stop': ['User:', '\n\n']  # Stop at natural breaks
                }
            )
            
            return response['response'].strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def translate_text(self, text, target_language="Spanish"):
        """AI translation"""
        try:
            prompt = f"Translate to {target_language}: {text}"
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={'num_predict': 100, 'temperature': 0.3}
            )
            return response['response'].strip()
        except:
            return "Translation error"
    
    def process_command(self, user_input):
        """Smart command processing"""
        start_time = time.time()
        
        # Add to history (keep last 4 exchanges)
        self.conversation_history.append(f"User: {user_input}")
        if len(self.conversation_history) > 8:
            self.conversation_history = self.conversation_history[-8:]
        
        # Determine if search is needed
        search_keywords = ['search', 'find', 'what is', 'who is', 'latest', 'news', 'current', 'today', 'recent', 'happening', 'update']
        needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
        
        # Also search for country/location + news combinations
        location_news = ['india news', 'news in', 'current news', 'breaking news', 'headlines']
        if any(phrase in user_input.lower() for phrase in location_news):
            needs_search = True
        
        if needs_search:
            print("🔍 Searching...")
            search_results = self.web_search(user_input)
            response = self.generate_response(user_input, search_results)
        elif "translate" in user_input.lower():
            # Extract text to translate
            text_to_translate = user_input.replace("translate", "").strip()
            response = self.translate_text(text_to_translate)
        else:
            # Regular conversation
            response = self.generate_response(user_input)
        
        # Add response to history
        self.conversation_history.append(f"AI: {response}")
        
        # Calculate performance
        response_time = time.time() - start_time
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Determine if GPU is being used
        performance = "🚀 GPU" if response_time < 3 else "💻 CPU"
        print(f"[{timestamp}] {performance} Response: {response_time:.1f}s")
        
        return response
    
    def run(self):
        """Main AI loop"""
        print("🤖 Updated AI System - All Features Enabled")
        print("Features: Chat, Search, Translation, Voice Output")
        print("Type 'exit' to quit\n")
        
        welcome_msg = "Updated AI system ready! I can chat, search the web, and translate languages."
        print(f"AI: {welcome_msg}")
        self.speak_async(welcome_msg)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye_msg = "Goodbye! Thanks for using the AI system!"
                    print(f"AI: {goodbye_msg}")
                    self.speak_async(goodbye_msg)
                    time.sleep(2)  # Wait for speech
                    break
                
                if user_input:
                    print("🤔 Thinking...")
                    response = self.process_command(user_input)
                    print(f"AI: {response}")
                    self.speak_async(response)
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                error_msg = "Sorry, I encountered an error. Please try again."
                print(f"AI: {error_msg}")
                self.speak_async(error_msg)

if __name__ == "__main__":
    ai = UpdatedAISystem()
    ai.run()