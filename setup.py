import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_offline.txt"])
    except:
        # Fallback to basic requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama", "duckduckgo-search", "edge-tts", "pygame", "requests"])

def install_edge_tts():
    """Install Edge TTS"""
    print("Installing Edge TTS...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts", "pygame"])
        print("✅ Edge TTS installed")
    except:
        print("❌ Edge TTS installation failed")

def install_ollama():
    """Install Ollama and download models"""
    print("Installing Ollama...")
    print("Please download Ollama from: https://ollama.ai/download")
    print("After installation, run these commands:")
    print("ollama pull phi3:mini")
    print("ollama pull gemma:2b")

def setup_system():
    """Complete system setup"""
    print("Setting up Revolutionary AI System...")
    
    # Install Python requirements
    install_requirements()
    
    # Install Edge TTS
    install_edge_tts()
    
    # Install Ollama
    install_ollama()
    
    print("\nSetup complete!")
    print("Run: python ai_system.py (Default with auto-reset)")

if __name__ == "__main__":
    setup_system()