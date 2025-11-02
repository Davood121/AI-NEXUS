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
        print("🤖 Initializing Self-Healing AI System...")
        
        # Auto-cleanup on startup
        self.auto_cleanup()
        
        # Initialize all variables first
        self.error_count = 0
        self.max_errors = 3
        self.last_heal_time = time.time()
        self.health_status = "healthy"
        self.conversation_history = []
        self.learning_score = 0
        self.edge_available = False
        
        # Load settings
        self.settings = self.load_default_settings()
        
        # Load knowledge base
        self.knowledge_base = self.load_knowledge_base()
        
        # Setup components
        self.setup_edge_tts()
        self.model = self.get_model()
        
        print(f"✅ Self-Healing AI System Ready - Model: {self.model}")
    
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
    
    def save_knowledge_base(self):
        """Save knowledge base"""
        try:
            self.knowledge_base['last_update'] = datetime.now().isoformat()
            with open('ai_knowledge_base.json', 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            print(f"Knowledge save error: {e}")
    
    def feed_data(self, data_input, data_type="text"):
        """Feed data to AI for learning"""
        try:
            print(f"🍽️ Feeding {data_type} data to AI...")
            
            # Process different data types
            if data_type == "url":
                content = self.extract_url_content(data_input)
            elif data_type == "file":
                content = self.extract_file_content(data_input)
            elif data_type == "image":
                content = self.extract_image_text(data_input)
            else:
                content = data_input
            
            if not content:
                print("❌ No content extracted")
                return False
            
            # Analyze content
            analysis = self.analyze_content(content)
            
            # Search for related information
            related_info = self.search_related_topics(analysis['key_topics'])
            
            # Store in knowledge base
            knowledge_entry = {
                'timestamp': datetime.now().isoformat(),
                'content': content[:1000],  # Store first 1000 chars
                'analysis': analysis,
                'related_searches': related_info,
                'reinforcement_score': 1.0,
                'usage_count': 0
            }
            
            self.knowledge_base['fed_data'].append(knowledge_entry)
            
            # Update learned concepts
            for topic in analysis['key_topics']:
                if topic in self.knowledge_base['learned_concepts']:
                    self.knowledge_base['learned_concepts'][topic] += 1
                else:
                    self.knowledge_base['learned_concepts'][topic] = 1
            
            self.save_knowledge_base()
            self.learning_score += 1
            
            print(f"✅ Data fed successfully! Learning score: {self.learning_score}")
            print(f"📚 Key topics learned: {', '.join(analysis['key_topics'][:3])}")
            
            return True
            
        except Exception as e:
            print(f"Data feeding error: {e}")
            return False
    
    def extract_url_content(self, url):
        """Extract content from URL"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 chars
            
        except Exception as e:
            print(f"URL extraction error: {e}")
            return None
    
    def extract_file_content(self, file_path):
        """Extract content from file"""
        try:
            # Check if it's an image file
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
            if any(file_path.lower().endswith(ext) for ext in image_extensions):
                return self.extract_image_text(file_path)
            
            # Regular text file
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:2000]
        except Exception as e:
            print(f"File extraction error: {e}")
            return None
    
    def extract_image_text(self, image_path):
        """Extract text from image using OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            print(f"📷 Extracting text from image: {image_path}")
            
            # Open and process image
            image = Image.open(image_path)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(image)
            
            if extracted_text.strip():
                print(f"✅ Extracted {len(extracted_text)} characters from image")
                return extracted_text[:2000]  # Limit to 2000 chars
            else:
                print("⚠️ No text found in image")
                return None
                
        except ImportError:
            print("❌ OCR not available - install: pip install pytesseract pillow")
            print("Also install Tesseract: https://github.com/tesseract-ocr/tesseract")
            return None
        except Exception as e:
            print(f"Image text extraction error: {e}")
            return None
    
    def analyze_content(self, content):
        """Analyze content to extract key information"""
        try:
            # Simple keyword extraction
            words = content.lower().split()
            
            # Filter common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
            
            filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
            
            # Count word frequency
            word_count = {}
            for word in filtered_words:
                word_count[word] = word_count.get(word, 0) + 1
            
            # Get top keywords
            key_topics = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
            key_topics = [topic[0] for topic in key_topics]
            
            return {
                'key_topics': key_topics,
                'word_count': len(words),
                'summary': content[:200] + '...' if len(content) > 200 else content
            }
            
        except Exception as e:
            print(f"Content analysis error: {e}")
            return {'key_topics': [], 'word_count': 0, 'summary': ''}
    
    def search_related_topics(self, topics):
        """Search for information related to extracted topics"""
        related_info = []
        
        for topic in topics[:2]:  # Search top 2 topics
            try:
                print(f"🔍 Searching related info for: {topic}")
                search_results = self.search_web(f"what is {topic}")
                if search_results:
                    related_info.extend(search_results[:1])  # Take 1 result per topic
            except:
                continue
        
        return related_info
    
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
            "ai_name": "ΛI-NEXUS",
            "auto_reset": True
        }
        
        try:
            if os.path.exists('ai_settings.json'):
                with open('ai_settings.json', 'r') as f:
                    settings = json.load(f)
                    # Ensure all default keys exist
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except:
            print("⚠️ Settings corrupted - resetting to defaults")
        
        self.save_settings(default_settings)
        return default_settings
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        try:
            if settings is None:
                settings = self.settings
            with open('ai_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
        except:
            pass
    
    def auto_cleanup(self):
        """Automatic cleanup on startup"""
        cleaned = 0
        
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
    
    def smart_cleanup(self):
        """Smart cleanup of unwanted files"""
        print("🧹 Running smart cleanup...")
        
        unwanted_files = [
            'temp_speech.mp3',
            'test_edge_neural.mp3'
        ]
        
        removed = 0
        
        # Remove specific files
        for file in unwanted_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    removed += 1
                except:
                    pass
        
        # Remove temp speech files
        try:
            for file in os.listdir('.'):
                if (file.startswith('temp_speech_') and file.endswith('.mp3') and 
                    file != f"temp_speech_{int(time.time())}.mp3"):  # Keep current
                    try:
                        os.remove(file)
                        removed += 1
                    except:
                        pass
        except:
            pass
        
        # Clean old log files
        try:
            for file in os.listdir('.'):
                if file.endswith('.log') or file.endswith('.tmp'):
                    try:
                        os.remove(file)
                        removed += 1
                    except:
                        pass
        except:
            pass
        
        return f"System optimized! Cleaned {removed} unwanted files for smoother performance."
    
    def reset_to_defaults(self):
        """Reset system to default settings"""
        print("🔄 Resetting to default settings...")
        
        default_settings = {
            "ai_model": "phi3:mini",
            "voice": "en-US-AriaNeural",
            "speech_enabled": True,
            "search_enabled": True,
            "response_length": 150,
            "temperature": 0.7,
            "ai_name": "ΛI-NEXUS",
            "auto_reset": True
        }
        
        self.settings = default_settings
        self.save_settings()
        self.setup_edge_tts()
        self.model = self.get_model()
        print("✅ Reset to defaults complete")
        self.error_count = 0
        self.health_status = "healthy"
    
    def heal_system(self):
        """Complete system healing with cleanup"""
        try:
            print("🔧 Running system diagnostics...")
            
            # Cleanup first
            self.smart_cleanup()
            
            # Reset components
            self.conversation_history = []
            self.learning_score = 0
            
            # Setup components
            self.setup_edge_tts()
            self.model = self.get_model()
            
            # Reset error tracking
            self.error_count = 0
            self.health_status = "healthy"
            self.last_heal_time = time.time()
            
            print("✅ System healing complete")
            
        except Exception as e:
            print(f"❌ System healing failed: {e}")
            self.health_status = "critical"
    
    def auto_heal(self, error_type="unknown"):
        """Automatic healing when errors occur"""
        self.error_count += 1
        current_time = time.time()
        
        print(f"🚑 Auto-healing triggered - Error #{self.error_count} ({error_type})")
        
        if self.error_count >= self.max_errors or (current_time - self.last_heal_time) > 300:
            print("🔄 Full system heal initiated...")
            self.heal_system()
        else:
            # Quick heal for specific component
            if "model" in error_type.lower():
                print("🤖 Healing AI model...")
                self.model = self.get_model()
            
            self.health_status = "recovering"
    
    def setup_edge_tts(self):
        """Setup Edge neural TTS"""
        self.edge_available = False
        
        if not self.settings["speech_enabled"]:
            print("🔇 Speech disabled")
            return
        
        if edge_tts is None:
            print("❌ Edge TTS not installed - Run: pip install edge-tts")
            return
        
        try:
            self.voice = self.settings["voice"]
            print(f"🔊 Edge TTS ready - Voice: {self.voice}")
            self.edge_available = True
        except Exception as e:
            print(f"❌ TTS error: {e}")
            self.edge_available = False
    
    def speak_edge(self, text):
        """Speak using Edge neural TTS with error recovery"""
        if not self.edge_available:
            return
        
        try:
            print("🗣️ Speaking...")
            asyncio.run(self._generate_speech(text))
            print("✅ Speech done")
        except Exception as e:
            print(f"Speech error: {e}")
            # Don't trigger auto-healing for speech errors
            pass
    
    async def _generate_speech(self, text):
        """Generate speech with Edge TTS"""
        # Clean text for speech
        clean_text = text.replace('\n', ' ').replace('\r', ' ').strip()
        if not clean_text:
            return
            
        communicate = edge_tts.Communicate(clean_text, self.voice)
        temp_file = f"temp_speech_{int(time.time())}.mp3"
        
        try:
            await communicate.save(temp_file)
            
            import subprocess
            import sys
            
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
            except:
                # Fallback to system player
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
        """Get working AI model with fallback"""
        try:
            model = self.settings["ai_model"]
            ollama.generate(model=model, prompt='test', options={'num_predict': 1})
            return model
        except:
            # Try fallback models
            for model in ['phi3:mini', 'gemma:2b', 'llama2:latest']:
                try:
                    ollama.generate(model=model, prompt='test', options={'num_predict': 1})
                    self.settings["ai_model"] = model
                    return model
                except:
                    continue
            return 'phi3:mini'
    
    def search_web(self, query):
        """Search web with multiple fallback methods"""
        if not self.settings["search_enabled"]:
            return []
        
        # Try multiple search methods
        search_methods = [
            self._search_ddgs,
            self._search_ddgs_lite,
            self._search_fallback
        ]
        
        for method in search_methods:
            try:
                results = method(query)
                if results:
                    print(f"🔍 Found {len(results)} results")
                    return results
            except Exception as e:
                continue
        
        print("📚 Working offline - using AI knowledge")
        return []
    
    def _search_ddgs(self, query):
        """Primary DDGS search"""
        with DDGS() as ddgs:
            results = []
            for i, result in enumerate(ddgs.text(query, max_results=3)):
                if i >= 3:
                    break
                results.append({
                    'title': result['title'],
                    'content': result['body'][:300]
                })
            return results
    
    def _search_ddgs_lite(self, query):
        """Lite DDGS search with different settings"""
        with DDGS(timeout=10) as ddgs:
            results = []
            for i, result in enumerate(ddgs.text(query, max_results=2, region='us-en')):
                if i >= 2:
                    break
                results.append({
                    'title': result['title'],
                    'content': result['body'][:250]
                })
            return results
    
    def _search_fallback(self, query):
        """Fallback search using requests"""
        import requests
        import json
        
        # Simple fallback search
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        results = []
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'Information'),
                'content': data['AbstractText'][:300]
            })
        
        return results
    
    def search_github(self, query):
        """Search GitHub repositories"""
        try:
            import requests
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
            response = requests.get(url)
            data = response.json()
            
            results = []
            for repo in data.get('items', [])[:3]:
                results.append({
                    'name': repo['name'],
                    'description': repo.get('description', 'No description'),
                    'url': repo['html_url'],
                    'stars': repo['stargazers_count']
                })
            return results
        except:
            return []
    
    def search_arxiv(self, query):
        """Search arXiv papers"""
        try:
            import requests
            import xml.etree.ElementTree as ET
            
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
            response = requests.get(url)
            root = ET.fromstring(response.content)
            
            results = []
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text[:200]
                results.append({'title': title, 'summary': summary})
            return results
        except:
            return []
    
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            import requests
            
            # Search for articles
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            response = requests.get(search_url)
            data = response.json()
            
            if 'extract' in data:
                return [{
                    'title': data['title'],
                    'content': data['extract'][:300],
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }]
            return []
        except:
            return []
    
    def should_search(self, user_input):
        """AI decides if search is needed"""
        # Simple keyword-based search detection
        search_triggers = [
            'news', 'latest', 'current', 'today', 'happening', 'recent',
            'what is', 'who is', 'when', 'where', 'how', 'why',
            'information', 'update', 'story', 'events'
        ]
        
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in search_triggers)
    
    def auto_search(self, user_input):
        """Automatically search multiple sources"""
        all_results = []
        
        # Search web
        web_results = self.search_web(user_input)
        all_results.extend(web_results)
        
        # Search Wikipedia for factual questions
        if any(word in user_input.lower() for word in ['what', 'who', 'when', 'where', 'how']):
            wiki_results = self.search_wikipedia(user_input)
            all_results.extend(wiki_results)
        
        # Search GitHub for code/tech questions
        if any(word in user_input.lower() for word in ['code', 'programming', 'software', 'library', 'framework']):
            github_results = self.search_github(user_input)
            if github_results:
                all_results.extend([{'title': f"GitHub: {r['name']}", 'content': f"{r['description']} - {r['url']}"} for r in github_results])
        
        # Search arXiv for research questions
        if any(word in user_input.lower() for word in ['research', 'study', 'algorithm', 'theory', 'analysis']):
            arxiv_results = self.search_arxiv(user_input)
            if arxiv_results:
                all_results.extend([{'title': f"Research: {r['title']}", 'content': r['summary']} for r in arxiv_results])
        
        return all_results[:5]  # Limit to top 5 results
    
    def get_response_length(self, user_input, search_results):
        """Determine response length based on query complexity"""
        # Detailed information keywords
        detailed_keywords = ['explain', 'details', 'information', 'tell me about', 'what is', 'how does', 'describe', 'news', 'current', 'latest']
        
        # Check if user wants detailed info
        wants_details = any(keyword in user_input.lower() for keyword in detailed_keywords)
        
        # Check if we have search results (more info available)
        has_search_data = search_results and len(search_results) > 0
        
        if wants_details and has_search_data:
            return 250  # Long detailed response
        elif has_search_data:
            return 180  # Medium response with search data
        elif wants_details:
            return 150  # Medium detailed response
        else:
            return 80   # Short response
    
    def generate_response(self, user_input, search_results=None):
        """Generate AI response with adaptive length"""
        try:
            # Determine response length based on query
            response_length = self.get_response_length(user_input, search_results)
            
            context = f"You are Lambda I-NEXUS. When search results are provided, ALWAYS use them to answer the question with current information. Do not mention knowledge limitations. Current time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n"
            
            # Add fed knowledge to context (only if relevant to query)
            fed_knowledge = self.use_fed_knowledge(user_input)
            if fed_knowledge and not any(word in user_input.lower() for word in ['who', 'creator', 'made', 'davood']):
                context += "KNOWLEDGE:\n"
                for i, knowledge in enumerate(fed_knowledge, 1):
                    context += f"{i}. {knowledge['analysis']['summary']}\n"
            elif fed_knowledge and any(word in user_input.lower() for word in ['who', 'creator', 'made', 'davood']):
                context += "CREATOR INFO:\n"
                for i, knowledge in enumerate(fed_knowledge, 1):
                    context += f"{i}. {knowledge['content'][:200]}\n"
            
            if search_results:
                context += "\n=== CURRENT WEB SEARCH RESULTS ===\n"
                for i, result in enumerate(search_results, 1):
                    context += f"Result {i}: {result['title']}\n{result['content'][:400]}\n\n"
                context += "=== END SEARCH RESULTS ===\n\nIMPORTANT: Use ONLY the above search results to answer. Provide specific details from the search results.\n"
            
            if self.conversation_history:
                context += "Recent conversation:\n"
                for msg in self.conversation_history[-4:]:
                    context += f"{msg}\n"
                context += "\n"
            
            if search_results:
                prompt = f"{context}\nUser Question: {user_input}\n\nAnswer based on the search results above. Be specific and detailed:\nΛI-NEXUS:"
            else:
                prompt = f"{context}\nUser: {user_input}\nΛI-NEXUS:"
            
            print(f"📝 Response length: {response_length} tokens")
            
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': max(response_length, 50),
                    'temperature': self.settings["temperature"],
                    'top_p': 0.9
                }
            )
            
            result = response['response'].strip()
            if not result:
                result = "I'm ΛI-NEXUS, your AI assistant. How can I help you?"
            return result
            
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            if hasattr(self, 'settings') and self.settings.get("auto_reset", False):
                self.auto_heal("model_error")
            return error_msg
    
    def run(self):
        """Main AI system loop with error recovery"""
        print("\n" + "="*60)
        print(f"🤖 ΛI-NEXUS - REVOLUTIONARY AI SYSTEM")
        print("Features: Self-Healing, Neural Voice, AI Auto-Search, Data Feeding, OCR")
        print("="*60)
        
        welcome = f"Hello! I'm ΛI-NEXUS, your self-improving AI assistant. Feed me data with 'feed [text/url/file/image]' and I'll learn from it! How can I help you?"
        print(f"\nAI: {welcome}")
        self.speak_edge(welcome)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    goodbye = "Goodbye! Your settings are saved and protected."
                    print(f"AI: {goodbye}")
                    self.speak_edge(goodbye)
                    break
                
                elif user_input.lower().startswith('feed '):
                    # Data feeding command
                    data = user_input[5:].strip()
                    if data.startswith('http'):
                        success = self.feed_data(data, "url")
                    elif os.path.exists(data):
                        # Check if it's an image
                        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
                        if any(data.lower().endswith(ext) for ext in image_extensions):
                            success = self.feed_data(data, "image")
                        else:
                            success = self.feed_data(data, "file")
                    else:
                        success = self.feed_data(data, "text")
                    
                    if success:
                        feed_msg = f"I've learned from that data! My knowledge base now has {len(self.knowledge_base['fed_data'])} entries."
                    else:
                        feed_msg = "I had trouble processing that data. Please try again."
                    
                    print(f"AI: {feed_msg}")
                    self.speak_edge(feed_msg)
                    continue
                
                elif user_input.lower() == 'knowledge':
                    # Show knowledge stats
                    stats = f"Knowledge Base Stats: {len(self.knowledge_base['fed_data'])} entries, Learning score: {self.learning_score}, Top concepts: {list(self.knowledge_base['learned_concepts'].keys())[:3]}"
                    print(f"AI: {stats}")
                    self.speak_edge(stats)
                    continue
                
                elif user_input.lower() == 'reset':
                    self.reset_to_defaults()
                    reset_msg = "I've been reset to default settings."
                    print(f"AI: {reset_msg}")
                    self.speak_edge(reset_msg)
                    continue
                
                elif user_input.lower() in ['cleanup', 'clean', 'optimize']:
                    cleanup_msg = self.smart_cleanup()
                    print(f"AI: {cleanup_msg}")
                    self.speak_edge(cleanup_msg)
                    continue
                
                if user_input:
                    start_time = time.time()
                    
                    # Add to conversation history
                    self.conversation_history.append(f"User: {user_input}")
                    
                    # AI decides if search is needed
                    search_results = []
                    if self.should_search(user_input):
                        print("🤖 AI decided to search for information...")
                        search_results = self.auto_search(user_input)
                        if not search_results:
                            print("📚 Working offline - using AI knowledge")
                    
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
                    
                    # Speak response
                    self.speak_edge(response)
                    
                    # Auto-save settings
                    self.save_settings()
                
            except KeyboardInterrupt:
                print("\n👋 AI System shutting down...")
                break
            except Exception as e:
                print(f"System error: {e}")
                if hasattr(self, 'settings') and self.settings.get("auto_reset", False):
                    self.auto_heal("critical_error")
                    error_msg = f"I've automatically healed from a critical error. System status: {self.health_status}"
                    print(f"AI: {error_msg}")
                    self.speak_edge(error_msg)

if __name__ == "__main__":
    ai = DefaultAISystem()
    ai.run()