import pyttsx3
import ollama
import time
from datetime import datetime

class SimpleAI:
    def __init__(self):
        # Simple TTS setup
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 200)
        
        print("Testing AI model...")
        try:
            test = ollama.generate(model='phi3:mini', prompt='Hi', options={'num_predict': 5})
            print("✅ AI model working!")
        except Exception as e:
            print(f"❌ Model error: {e}")
            print("Make sure to run: ollama pull phi3:mini")
    
    def speak(self, text):
        """Simple blocking speech"""
        print(f"AI: {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            print("(Speech not available)")
    
    def get_response(self, user_input):
        """Get AI response"""
        try:
            start_time = time.time()
            
            response = ollama.generate(
                model='phi3:mini',
                prompt=f"User: {user_input}\nAI:",
                options={
                    'num_predict': 50,
                    'temperature': 0.7
                }
            )
            
            response_time = time.time() - start_time
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            result = response['response'].strip()
            print(f"[{timestamp}] Response time: {response_time:.1f}s")
            
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self):
        print("Simple AI System Ready")
        print("Type 'exit' to quit\n")
        
        self.speak("Simple AI ready!")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.speak("Goodbye!")
                    break
                
                if user_input:
                    response = self.get_response(user_input)
                    self.speak(response)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    ai = SimpleAI()
    ai.run()