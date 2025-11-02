import sys
import os

def main():
    print("=== URL Feeding Guide ===")
    print()
    print("To feed URLs to your AI, you have 2 options:")
    print()
    print("Option 1 - Run AI system and use feed command:")
    print("1. Open command prompt in this folder")
    print("2. Run: python ai_system.py")
    print("3. When AI starts, type: feed https://en.wikipedia.org/wiki/Article_(grammar)")
    print()
    print("Option 2 - Use direct URL feeder:")
    print("1. Open command prompt in this folder") 
    print("2. Run: python simple_url_feed.py")
    print()
    print("DON'T type 'python simple_url_feed.py' as a message to the AI!")
    print("That's a terminal command, not a chat message.")
    print()
    
    # Quick test of URL feeding
    url = "https://en.wikipedia.org/wiki/Article_(grammar)"
    
    try:
        import requests
        from bs4 import BeautifulSoup
        import json
        from datetime import datetime
        
        print(f"Testing URL extraction: {url}")
        
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        clean_text = ' '.join(text.split())[:1000]  # First 1000 chars
        
        print(f"✅ Successfully extracted {len(clean_text)} characters")
        print(f"Preview: {clean_text[:200]}...")
        
        # Save to knowledge base
        kb_file = 'ai_knowledge_base.json'
        try:
            with open(kb_file, 'r') as f:
                kb = json.load(f)
        except:
            kb = {'fed_data': [], 'learned_concepts': {}}
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source_url': url,
            'content': clean_text,
            'analysis': {'key_topics': ['article', 'grammar', 'language'], 'summary': 'Wikipedia article about grammar articles'},
            'reinforcement_score': 1.0,
            'usage_count': 0
        }
        
        kb['fed_data'].append(entry)
        
        with open(kb_file, 'w') as f:
            json.dump(kb, f, indent=2)
        
        print(f"✅ URL data saved to knowledge base!")
        print(f"Total entries: {len(kb['fed_data'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()