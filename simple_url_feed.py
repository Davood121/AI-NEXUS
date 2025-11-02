import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def extract_and_save_url(url):
    try:
        print(f"Extracting data from: {url}")
        
        # Get webpage content
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get clean text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract key topics
        words = clean_text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        word_count = {}
        for word in filtered_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        key_topics = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
        key_topics = [topic[0] for topic in key_topics]
        
        # Create knowledge entry
        knowledge_entry = {
            'timestamp': datetime.now().isoformat(),
            'source_url': url,
            'content': clean_text[:2000],  # First 2000 chars
            'full_content': clean_text,    # Full content
            'analysis': {
                'key_topics': key_topics,
                'word_count': len(words),
                'summary': clean_text[:300] + '...' if len(clean_text) > 300 else clean_text
            },
            'reinforcement_score': 1.0,
            'usage_count': 0
        }
        
        # Load existing knowledge base
        try:
            if os.path.exists('ai_knowledge_base.json'):
                with open('ai_knowledge_base.json', 'r') as f:
                    kb = json.load(f)
            else:
                kb = {'fed_data': [], 'learned_concepts': {}}
        except:
            kb = {'fed_data': [], 'learned_concepts': {}}
        
        # Add new entry
        kb['fed_data'].append(knowledge_entry)
        
        # Update learned concepts
        for topic in key_topics:
            kb['learned_concepts'][topic] = kb['learned_concepts'].get(topic, 0) + 1
        
        # Save knowledge base
        with open('ai_knowledge_base.json', 'w') as f:
            json.dump(kb, f, indent=2)
        
        print("SUCCESS: URL data extracted and saved!")
        print(f"Extracted {len(clean_text)} characters")
        print(f"Key topics: {', '.join(key_topics[:3])}")
        print(f"Knowledge base now has {len(kb['fed_data'])} entries")
        
        return True
        
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return False

# Feed the Wikipedia URL
url = "https://en.wikipedia.org/wiki/Article_(grammar)"
extract_and_save_url(url)