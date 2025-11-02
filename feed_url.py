import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def feed_url_to_ai():
    try:
        # Import the AI system
        from ai_system import DefaultAISystem
        
        print("Initializing AI system...")
        ai = DefaultAISystem()
        
        # URL to feed
        url = "https://en.wikipedia.org/wiki/Article_(grammar)"
        
        print(f"Feeding URL: {url}")
        
        # Feed the URL data
        success = ai.feed_data(url, "url")
        
        if success:
            print("SUCCESS: URL data extracted and saved!")
            print(f"Knowledge base now has {len(ai.knowledge_base['fed_data'])} entries")
        else:
            print("FAILED: Could not extract data from URL")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    feed_url_to_ai()