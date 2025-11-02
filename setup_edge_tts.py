import subprocess
import sys
import asyncio
import os

def install_edge_tts():
    """Install Edge TTS"""
    print("Installing Edge TTS...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts", "pygame"])
        print("✅ Edge TTS installed")
        return True
    except Exception as e:
        print(f"❌ Edge TTS installation failed: {e}")
        return False

async def test_edge_tts():
    """Test Edge TTS"""
    print("Testing Edge neural TTS...")
    try:
        import edge_tts
        import pygame
        
        # Generate test speech
        voice = "en-US-AriaNeural"
        text = "This is a test of Microsoft Edge neural text-to-speech. The voice quality should be very natural and human-like."
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save("test_edge_neural.mp3")
        
        print("✅ Edge TTS test successful!")
        print("🔊 Generated test_edge_neural.mp3 - play it to hear the neural voice")
        return True
        
    except Exception as e:
        print(f"❌ Edge TTS test error: {e}")
        return False

def main():
    print("🤖 EDGE NEURAL TTS SETUP")
    print("="*40)
    
    # Install Edge TTS
    if not install_edge_tts():
        return
    
    # Test Edge TTS
    if asyncio.run(test_edge_tts()):
        print("\n✅ SETUP COMPLETE!")
        print("Run: python ai_with_edge_tts.py")
    else:
        print("\n❌ Setup incomplete - check errors above")

if __name__ == "__main__":
    main()