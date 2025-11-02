import subprocess
import json
import os

def check_ai_hardware():
    """Check if AI is running on CPU or GPU"""
    print("🔍 Checking AI Hardware Configuration...")
    print("="*50)
    
    # Check Ollama status
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📊 Ollama Models Status:")
            print(result.stdout)
        else:
            print("❌ Ollama not running")
    except:
        print("❌ Ollama not found")
    
    # Check GPU availability
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🎮 GPU Available: {gpu_name}")
            print(f"🔢 GPU Count: {gpu_count}")
            print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("💻 Running on CPU only")
    except ImportError:
        print("💻 PyTorch not installed - likely CPU only")
    
    # Check system info
    try:
        import psutil
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        print(f"🖥️ CPU Cores: {cpu_count}")
        print(f"💾 RAM: {memory.total / 1024**3:.1f} GB")
        print(f"📈 RAM Usage: {memory.percent}%")
    except ImportError:
        print("📊 System info not available")
    
    # Check Ollama configuration
    try:
        # Check if CUDA is being used by Ollama
        result = subprocess.run(['ollama', 'show', 'phi3:mini'], capture_output=True, text=True)
        if 'cuda' in result.stdout.lower() or 'gpu' in result.stdout.lower():
            print("🚀 Ollama using GPU acceleration")
        else:
            print("🐌 Ollama using CPU")
    except:
        pass
    
    print("\n" + "="*50)
    print("💡 Performance Tips:")
    print("- GPU: 1-3 seconds response time")
    print("- CPU: 5-15 seconds response time")
    print("- For GPU: Install CUDA drivers")
    print("- For better CPU: Use phi3:mini model")

if __name__ == "__main__":
    check_ai_hardware()