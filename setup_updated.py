import subprocess
import sys
import os

def install_dependencies():
    """Install all required packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        'pyttsx3',
        'ollama', 
        'duckduckgo-search',
        'requests'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except:
            print(f"❌ Failed to install {package}")

def download_models():
    """Download optimized AI models"""
    print("\n🤖 Downloading AI models...")
    
    models = [
        'gemma:2b',      # Ultra fast
        'phi3:mini',     # Fast and smart
        'llama2:latest'  # Backup
    ]
    
    for model in models:
        try:
            print(f"Downloading {model}...")
            subprocess.run(['ollama', 'pull', model], check=True)
            print(f"✅ {model} downloaded")
        except:
            print(f"⚠️ {model} download failed (will try at runtime)")

def check_system():
    """Check system requirements"""
    print("\n🔍 System Check:")
    
    # Check Python
    python_version = sys.version.split()[0]
    print(f"Python: {python_version}")
    
    # Check Ollama
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        print(f"Ollama: {result.stdout.strip()}")
    except:
        print("❌ Ollama not found - install from https://ollama.ai")
        return False
    
    # Check GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if 'RTX 4050' in result.stdout:
            print("✅ RTX 4050 detected")
        else:
            print("💻 Using CPU (GPU not detected)")
    except:
        print("💻 Using CPU (nvidia-smi not found)")
    
    return True

def main():
    """Complete setup process"""
    print("🚀 Setting up Updated AI System\n")
    
    # Check system
    if not check_system():
        print("\n❌ System check failed")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Download models
    download_models()
    
    print("\n" + "="*50)
    print("✅ Setup Complete!")
    print("\n🎯 To run your AI:")
    print("python updated_ai_system.py")
    print("\n🌟 Features:")
    print("- Smart conversation with memory")
    print("- Real-time web search")
    print("- Multi-language translation") 
    print("- Voice output with timestamps")
    print("- Auto-detects fastest model")
    print("- Complete responses (no cutoff)")
    print("- GPU acceleration (if available)")

if __name__ == "__main__":
    main()