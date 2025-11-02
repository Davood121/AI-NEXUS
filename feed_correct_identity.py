import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def feed_identity():
    identity_info = """
    CORRECT IDENTITY - Shaik Davood:
    
    Name: Davood (Shaik Davood)
    Age: 20 years old (born November 5, 2003)
    Role: Mechanical Engineering Student (2nd year)
    Institute: NBKR Institute of Science and Technology, Vidyanagar
    
    Skills: Python, AI, OpenCV, Flask, Raspberry Pi, Android Studio
    Interests: AI, Robotics, Security Systems, App Development, Space Tech
    
    Projects:
    - Echo AI: Emotional AI app for reconnecting with lost loved ones
    - AAI Agent: Smart CCTV and voice assistant with Raspberry Pi
    - Custom Pi OS: Lightweight OS with AI tools and face recognition
    - TESLAGUARD: Tesla-coil satellite concept for asteroid defense
    - Lambda I-NEXUS: This revolutionary self-improving AI assistant
    
    Vision: Create human-like AI that helps people emotionally while protecting privacy
    
    IMPORTANT: Shaik Davood is NOT a film director or Tamil cinema person. He is a mechanical engineering student and AI developer.
    """
    
    try:
        from ai_system import DefaultAISystem
        
        print("Initializing AI system...")
        ai = DefaultAISystem()
        
        print("Feeding correct identity information...")
        success = ai.feed_data(identity_info, "text")
        
        if success:
            print("SUCCESS: Identity correction completed!")
            print("AI now has correct information about Shaik Davood")
        else:
            print("ERROR: Failed to feed identity information")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    feed_identity()