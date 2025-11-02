import os
import shutil
import zipfile
from datetime import datetime

def quick_backup():
    """Quick one-click backup of AI system"""
    ai_folder = r"c:\Users\shaik\Desktop\ΛI-NEXUSdAi"
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"ai_quick_backup_{timestamp}.zip"
    backup_path = os.path.join(ai_folder, backup_name)
    
    # Files to backup
    important_files = [
        "updated_ai_system.py",
        "setup_updated.py",
        "simple_ai.py", 
        "final_ai.py",
        "requirements.txt",
        "README_UPDATED.md"
    ]
    
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            backed_up = 0
            for file in important_files:
                file_path = os.path.join(ai_folder, file)
                if os.path.exists(file_path):
                    zipf.write(file_path, file)
                    print(f"✅ {file}")
                    backed_up += 1
        
        print(f"\n🎉 Quick backup complete!")
        print(f"📦 File: {backup_name}")
        print(f"📊 Files: {backed_up}")
        print(f"📍 Location: {ai_folder}")
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")

if __name__ == "__main__":
    print("🚀 Quick AI Backup")
    print("=" * 30)
    quick_backup()