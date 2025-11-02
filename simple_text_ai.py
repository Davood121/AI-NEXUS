try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
from datetime import datetime

class SimpleTextAI:
    def __init__(self):
        print("🤖 Starting Simple Text AI...")
        
        # Get working model
        self.model = self.get_model()
        self.conversation_history = []
        
        print(f"✅ AI Ready - Model: {self.model}")
        print("📝 Text-only mode (no speech issues)")
    
    def get_model(self):
        """Get working model"""
        models = ['phi3:mini', 'gemma:2b', 'llama2:latest']
        for model in models:
            try:
                ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                return model
            except:
                continue
        return 'phi3:mini'
    
    def search_web(self, query):
        """Simple web search"""
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
            # Check if search needed
            search_words = ['search', 'find', 'what is', 'who is', 'latest', 'news', 'current', 'today']
            needs_search = any(word in user_input.lower() for word in search_words)
            
            # Build context
            context = f"Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            # Add search info if needed
            if needs_search:
                search_info = self.search_web(user_input)
                if search_info:
                    context += f"Search information: {search_info}\n"
            
            # Add recent conversation
            if self.conversation_history:
                context += "Recent conversation:\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\n"
            
            # Create prompt
            prompt = f"{context}\nUser: {user_input}\nAI:"
            
            # Generate response
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': 120,
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            )
            
            return response['response'].strip()
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def run(self):
        """Main AI loop"""
        print("\n" + "="*50)
        print("🤖 SIMPLE TEXT AI SYSTEM")
        print("Features: Chat, Web Search (No Speech Issues)")
        print("="*50)
        
        print("\nAI: Hello! I'm ΛI-NEXUS, your text-based AI assistant. I can chat and search the web. How can I help you?")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("AI: Goodbye! Thanks for chatting with me!")
                    break
                
                if user_input:
                    # Add to history
                    self.conversation_history.append(f"User: {user_input}")
                    
                    # Get response
                    start_time = time.time()
                    response = self.get_response(user_input)
                    response_time = time.time() - start_time
                    
                    # Add to history
                    self.conversation_history.append(f"AI: {response}")
                    
                    # Keep history manageable
                    if len(self.conversation_history) > 8:
                        self.conversation_history = self.conversation_history[-8:]
                    
                    # Show response
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"AI: Sorry, I encountered an error: {str(e)}")

if __name__ == "__main__":
    ai = SimpleTextAI()
    ai.run()