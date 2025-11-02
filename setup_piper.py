import subprocess
import sys
import os
import urllib.request

def install_piper():
    """Install Piper TTS"""
    print("Installing Piper TTS...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "piper-tts", "pygame", "wave"])
        print("✅ Piper TTS installed")
    except Exception as e:
        print(f"❌ Piper installation failed: {e}")
        return False
    return True

def download_voice_model():
    """Download Amy voice model"""
    print("Downloading neural voice model...")
    
    # Create directory
    os.makedirs("piper_voice_models", exist_ok=True)
    
    # Model files
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/"
    files = [
        "en_US-amy-medium.onnx",
        "en_US-amy-medium.onnx.json"
    ]
    
    for file in files:
        file_path = f"piper_voice_models/{file}"
        if os.path.exists(file_path):
            print(f"✅ {file} already exists")
            continue
        
        try:
            print(f"📥 Downloading {file}...")
            urllib.request.urlretrieve(f"{base_url}{file}", file_path)
            print(f"✅ Downloaded {file}")
        except Exception as e:
            print(f"❌ Failed to download {file}: {e}")
            return False
    
    return True

def test_piper():
    """Test Piper TTS"""
    print("Testing Piper TTS...")
    try:
        from piper import PiperVoice
        import wave
        
        # Load voice model
        voice = PiperVoice.load("piper_voice_models/en_US-amy-medium.onnx")
        
        # Generate test audio
        audio_data = b''
        for audio_chunk in voice.synthesize("This is a test of the neural voice system."):
            audio_data += audio_chunk
        
        # Save test file
        with wave.open("test_neural.wav", 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            wav_file.writeframes(audio_data)
        
        print("✅ Piper TTS test successful!")
        print("🔊 Generated test_neural.wav - play it to hear the neural voice")
        return True
        
    except Exception as e:
        print(f"❌ Piper test error: {e}")
        return False

def main():
    print("🤖 PIPER NEURAL TTS SETUP")
    print("="*40)
    
    # Install Piper
    if not install_piper():
        return
    
    # Download voice model
    if not download_voice_model():
        return
    
    # Test Piper
    if test_piper():
        print("\n✅ SETUP COMPLETE!")
        print("Run: python ai_with_piper_tts.py")
    else:
        print("\n❌ Setup incomplete - check errors above")

if __name__ == "__main__":
    main()