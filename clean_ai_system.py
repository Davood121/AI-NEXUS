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

class CleanAISystem:
    def __init__(self):
        print("Initializing AI System...")
        
        # Load settings and knowledge base
        self.settings = self.load_default_settings()
        self.knowledge_base = self.load_knowledge_base()
        self.conversation_history = []
        self.learning_score = len(self.knowledge_base.get('fed_data', []))
        
        # Setup components
        self.setup_edge_tts()
        self.model = self.get_model()
        
        print(f"AI System Ready - Model: {self.model}")
    
    def load_knowledge_base(self):
        """Load AI knowledge base"""
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
    
    def use_fed_knowledge(self, query):
        """Use fed knowledge to enhance responses"""
        relevant_knowledge = []
        query_words = query.lower().split()
        
        # Special handling for identity queries about Shaik Davood
        if any(word in query.lower() for word in ['shaik', 'davood', 'creator', 'who created', 'who made', 'who is']):
            for entry in self.knowledge_base['fed_data']:
                if any(word in entry['content'].lower() for word in ['shaik', 'davood', 'mechanical', 'engineering', 'nbkr']):
                    relevant_knowledge.append(entry)
                    entry['usage_count'] += 1
                    entry['reinforcement_score'] += 0.2
        
        # General knowledge search
        for entry in self.knowledge_base['fed_data']:
            for topic in entry['analysis']['key_topics']:
                if any(word in topic for word in query_words):
                    if entry not in relevant_knowledge:
                        relevant_knowledge.append(entry)
                        entry['usage_count'] += 1
                        entry['reinforcement_score'] += 0.1
                    break
        
        # Sort by reinforcement score
        relevant_knowledge.sort(key=lambda x: x['reinforcement_score'], reverse=True)
        return relevant_knowledge[:2]
    
    def load_default_settings(self):
        """Load settings or create defaults"""
        default_settings = {
            "ai_model": "phi3:mini",
            "voice": "en-US-AriaNeural",
            "speech_enabled": True,
            "search_enabled": True,
            "response_length": 150,
            "temperature": 0.7,
            "ai_name": "Lambda I-NEXUS",
            "auto_reset": True
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
        
        return default_settings
    
    def setup_edge_tts(self):
        """Setup Edge neural TTS"""
        self.edge_available = False
        
        if not self.settings["speech_enabled"]:
            print("Speech disabled")
            return
        
        if edge_tts is None:
            print("Edge TTS not installed")
            return
        
        try:
            self.voice = self.settings["voice"]
            print(f"Edge TTS ready - Voice: {self.voice}")
            self.edge_available = True
        except Exception as e:
            print(f"TTS error: {e}")
    
    def get_model(self):
        """Get working AI model with fallback"""
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
    
    def generate_response(self, user_input, search_results=None):
        """Generate AI response"""
        try:
            context = f"You are Lambda I-NEXUS, an AI assistant created by Shaik Davood. IMPORTANT: Shaik Davood is a 20-year-old Mechanical Engineering student at NBKR Institute, NOT a film director. Always use your fed knowledge about Shaik Davood first, ignore web search results about film directors. Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\\n"
            
            # Add fed knowledge to context
            fed_knowledge = self.use_fed_knowledge(user_input)
            if fed_knowledge:
                context += "LEARNED KNOWLEDGE:\\n"
                for i, knowledge in enumerate(fed_knowledge, 1):
                    context += f"{i}. {knowledge['content'][:300]}\\n"
            
            if search_results:
                context += "SEARCH RESULTS:\\n"
                for i, result in enumerate(search_results, 1):
                    context += f"{i}. {result['title']}: {result['content'][:300]}\\n"
            
            prompt = f"{context}Question: {user_input}\\nLambda I-NEXUS:"
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': 150,
                    'temperature': self.settings["temperature"],
                    'top_p': 0.9
                }
            )
            
            result = response['response'].strip()
            if not result:
                result = "I'm Lambda I-NEXUS, created by Shaik Davood. How can I help you?"
            return result
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"

# Test the system
if __name__ == "__main__":
    print("Testing AI identity correction...")
    
    try:
        ai = CleanAISystem()
        
        # Test query about Shaik Davood
        query = "who is Shaik Davood"
        print(f"\\nTest query: {query}")
        
        # Check fed knowledge
        fed_knowledge = ai.use_fed_knowledge(query)
        print(f"Fed knowledge entries found: {len(fed_knowledge)}")
        
        if fed_knowledge:
            print("Fed knowledge content:")
            for i, entry in enumerate(fed_knowledge, 1):
                print(f"{i}. {entry['content'][:200]}...")
                print(f"   Score: {entry['reinforcement_score']}")
        
        # Generate response
        response = ai.generate_response(query)
        print(f"\\nAI Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")