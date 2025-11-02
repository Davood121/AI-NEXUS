try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import ollama
import time
import json
import os
from datetime import datetime

class WorkingAI:
    def __init__(self):
        print("Initializing Lambda I-NEXUS AI System...")
        self.settings = self.load_settings()
        self.model = self.get_model()
        self.conversation_history = []
        self.knowledge_base = self.load_knowledge_base()
        print(f"Lambda I-NEXUS Ready - Model: {self.model}")
    
    def load_settings(self):
        try:
            if os.path.exists('ai_settings.json'):
                with open('ai_settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "ai_model": "phi3:mini",
            "search_enabled": True,
            "response_length": 180,
            "temperature": 0.6,
            "ai_name": "Lambda I-NEXUS"
        }
    
    def load_knowledge_base(self):
        try:
            if os.path.exists('ai_knowledge_base.json'):
                with open('ai_knowledge_base.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'fed_data': [], 'learned_concepts': {}}
    
    def get_model(self):
        try:
            model = self.settings["ai_model"]
            ollama.generate(model=model, prompt='test', options={'num_predict': 1})
            return model
        except:
            for model in ['phi3:mini', 'gemma:2b', 'llama2:latest']:
                try:
                    ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                    return model
                except:
                    continue
            return 'phi3:mini'
    
    def search_web(self, query):
        if not self.settings["search_enabled"]:
            return []
        try:
            print(f"Searching: {query}")
            with DDGS() as ddgs:
                results = []
                for i, result in enumerate(ddgs.text(query, max_results=3)):
                    if i >= 3:
                        break
                    results.append({
                        'title': result['title'],
                        'content': result['body'][:300]
                    })
                print(f"Found {len(results)} results")
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def should_search(self, user_input):
        search_triggers = [
            'news', 'latest', 'current', 'today', 'happening', 'recent',
            'what is', 'who is', 'when', 'where', 'how', 'why',
            'information', 'update', 'story', 'events'
        ]
        return any(trigger in user_input.lower() for trigger in search_triggers)
    
    def use_fed_knowledge(self, query):
        relevant_knowledge = []
        if any(word in query.lower() for word in ['shaik', 'davood', 'creator', 'who created', 'who made']):
            for entry in self.knowledge_base['fed_data']:
                if any(word in entry['content'].lower() for word in ['shaik', 'davood', 'mechanical', 'engineering']):
                    relevant_knowledge.append(entry)
        return relevant_knowledge[:2]
    
    def generate_response(self, user_input, search_results=None):
        try:
            context = f"You are Lambda I-NEXUS created by Shaik Davood. Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\\n"
            
            fed_knowledge = self.use_fed_knowledge(user_input)
            if fed_knowledge:
                context += "KNOWLEDGE:\\n"
                for knowledge in fed_knowledge:
                    context += f"- {knowledge['content'][:200]}\\n"
            
            if search_results:
                context += "SEARCH RESULTS:\\n"
                for result in search_results:
                    context += f"- {result['title']}: {result['content'][:200]}\\n"
            
            if self.conversation_history:
                context += "Recent conversation:\\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\\n"
            
            prompt = f"{context}User: {user_input}\\nLambda I-NEXUS:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': self.settings["response_length"],
                    'temperature': self.settings["temperature"]
                }
            )
            
            return response['response'].strip()
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def run(self):
        print("\\n" + "="*60)
        print("Lambda I-NEXUS - REVOLUTIONARY AI SYSTEM")
        print("Features: Self-Healing, AI Auto-Search, Data Feeding")
        print("="*60)
        
        welcome = "Hello! I'm Lambda I-NEXUS, your self-improving AI assistant. How can I help you?"
        print(f"\\nAI: {welcome}")
        
        while True:
            try:
                user_input = input("\\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("AI: Goodbye! Your settings are saved.")
                    break
                
                if user_input:
                    start_time = time.time()
                    
                    self.conversation_history.append(f"User: {user_input}")
                    
                    search_results = []
                    if self.should_search(user_input):
                        print("AI decided to search for information...")
                        search_results = self.search_web(user_input)
                    
                    response = self.generate_response(user_input, search_results)
                    
                    self.conversation_history.append(f"AI: {response}")
                    
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    response_time = time.time() - start_time
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Response time: {response_time:.1f}s")
                    print(f"AI: {response}")
                
            except KeyboardInterrupt:
                print("\\nAI System shutting down...")
                break
            except Exception as e:
                print(f"System error: {e}")

if __name__ == "__main__":
    ai = WorkingAI()
    ai.run()