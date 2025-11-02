try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
from datetime import datetime

class TextOnlyAI:
    def __init__(self):
        print("🤖 Initializing Text-Only AI System...")
        
        # AI settings
        self.model = self.get_model()
        self.conversation_history = []
        self.knowledge_base = self.load_knowledge()
        
        print(f"✅ AI System Ready - Model: {self.model}")
    
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
    
    def load_knowledge(self):
        """Load AI knowledge base"""
        try:
            if os.path.exists('ai_knowledge.json'):
                with open('ai_knowledge.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'facts': [], 'searches': []}
    
    def save_knowledge(self):
        """Save knowledge base"""
        try:
            with open('ai_knowledge.json', 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except:
            pass
    
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
                
                # Save search to knowledge
                self.knowledge_base['searches'].append({
                    'query': query,
                    'timestamp': datetime.now().isoformat(),
                    'results_count': len(results)
                })
                
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def generate_response(self, user_input, search_results=None):
        """Generate AI response"""
        try:
            # Build context
            context = f"Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            if search_results:
                context += "Search information:\n"
                for result in search_results:
                    context += f"- {result['title']}: {result['content'][:200]}...\n"
                context += "\n"
            
            # Add recent conversation
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
    
    def process_input(self, user_input):
        """Process user input and generate response"""
        start_time = time.time()
        
        # Add to conversation history
        self.conversation_history.append(f"User: {user_input}")
        
        # Check if search is needed
        search_keywords = ['search', 'find', 'what is', 'who is', 'latest', 'news', 'current', 'today', 'recent']
        needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
        
        # Search if needed
        search_results = []
        if needs_search:
            search_results = self.search_web(user_input)
        
        # Generate response
        response = self.generate_response(user_input, search_results)
        
        # Add to conversation history
        self.conversation_history.append(f"AI: {response}")
        
        # Keep conversation history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        # Save knowledge
        self.save_knowledge()
        
        # Calculate response time
        response_time = time.time() - start_time
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"[{timestamp}] Response time: {response_time:.1f}s")
        
        return response
    
    def run(self):
        """Main AI system loop"""
        print("\n" + "="*60)
        print("🤖 TEXT-ONLY AI SYSTEM")
        print("Features: Chat, Web Search, Knowledge Base")
        print("="*60)
        
        # Welcome message
        welcome = "Hello! I'm ΛI-NEXUS, your text-only AI assistant. I can chat, search the web, and remember our conversations. How can I help you today?"
        print(f"\nAI: {welcome}")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Thank you for using the AI system. Have a great day!"
                    print(f"AI: {goodbye}")
                    break
                
                if user_input:
                    # Process input and get response
                    response = self.process_input(user_input)
                    
                    # Display response
                    print(f"AI: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 AI System shutting down...")
                break
            except Exception as e:
                error_msg = "I'm sorry, I encountered an error. Please try again."
                print(f"AI: {error_msg}")

if __name__ == "__main__":
    ai = TextOnlyAI()
    ai.run()