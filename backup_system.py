import os
import shutil
import zipfile
from datetime import datetime
import json

class AIBackupSystem:
    def __init__(self):
        self.ai_folder = r"c:\Users\shaik\Desktop\ΛI-NEXUSdAi"
        self.backup_folder = os.path.join(self.ai_folder, "backups")
        self.ensure_backup_folder()
        
    def ensure_backup_folder(self):
        """Create backup folder if it doesn't exist"""
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
            print(f"✅ Created backup folder: {self.backup_folder}")
    
    def get_ai_files(self):
        """Get list of AI system files to backup"""
        ai_files = [
            "updated_ai_system.py",
            "setup_updated.py", 
            "simple_ai.py",
            "force_gpu_ai.py",
            "final_ai.py",
            "lightning_ai.py",
            "ultra_fast_ai.py",
            "gpu_ai_system.py",
            "fast_ai_system.py",
            "text_ai_system.py",
            "ai_system.py",
            "web_interface.py",
            "system_checker.py",
            "gpu_check.py",
            "requirements.txt",
            "simple_requirements.txt",
            "README.md",
            "README_UPDATED.md",
            "enable_gpu.bat"
        ]
        
        # Only include files that exist
        existing_files = []
        for file in ai_files:
            file_path = os.path.join(self.ai_folder, file)
            if os.path.exists(file_path):
                existing_files.append(file)
        
        return existing_files
    
    def create_backup(self, backup_name=None):
        """Create a backup of all AI files"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"ai_backup_{timestamp}"
        
        backup_zip = os.path.join(self.backup_folder, f"{backup_name}.zip")
        
        try:
            with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                ai_files = self.get_ai_files()
                
                for file in ai_files:
                    file_path = os.path.join(self.ai_folder, file)
                    zipf.write(file_path, file)
                    print(f"📁 Backed up: {file}")
                
                # Create backup info
                backup_info = {
                    "backup_date": datetime.now().isoformat(),
                    "files_count": len(ai_files),
                    "files": ai_files,
                    "backup_name": backup_name
                }
                
                # Add backup info to zip
                zipf.writestr("backup_info.json", json.dumps(backup_info, indent=2))
            
            print(f"\n✅ Backup created successfully!")
            print(f"📦 Backup file: {backup_zip}")
            print(f"📊 Files backed up: {len(ai_files)}")
            return backup_zip
            
        except Exception as e:
            print(f"❌ Backup failed: {str(e)}")
            return None
    
    def list_backups(self):
        """List all available backups"""
        if not os.path.exists(self.backup_folder):
            print("❌ No backup folder found")
            return []
        
        backups = []
        for file in os.listdir(self.backup_folder):
            if file.endswith('.zip'):
                file_path = os.path.join(self.backup_folder, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                backups.append({
                    'name': file,
                    'path': file_path,
                    'size': f"{file_size:.1f} KB",
                    'date': file_date.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        if backups:
            print(f"\n📦 Available Backups ({len(backups)}):")
            print("-" * 60)
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['name']}")
                print(f"   Date: {backup['date']}")
                print(f"   Size: {backup['size']}")
                print()
        else:
            print("❌ No backups found")
        
        return backups
    
    def restore_backup(self, backup_name):
        """Restore from a backup"""
        backup_path = os.path.join(self.backup_folder, backup_name)
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        try:
            # Create restore confirmation
            print(f"⚠️  This will overwrite existing AI files!")
            confirm = input("Type 'YES' to confirm restore: ")
            
            if confirm.upper() != 'YES':
                print("❌ Restore cancelled")
                return False
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Extract all files
                for file in zipf.namelist():
                    if file != 'backup_info.json':
                        zipf.extract(file, self.ai_folder)
                        print(f"📁 Restored: {file}")
                
                # Show backup info if available
                try:
                    backup_info = json.loads(zipf.read('backup_info.json'))
                    print(f"\n✅ Restore completed!")
                    print(f"📅 Backup date: {backup_info['backup_date']}")
                    print(f"📊 Files restored: {backup_info['files_count']}")
                except:
                    print(f"\n✅ Restore completed!")
            
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {str(e)}")
            return False
    
    def auto_backup(self):
        """Create automatic backup with timestamp"""
        print("🔄 Creating automatic backup...")
        return self.create_backup()
    
    def cleanup_old_backups(self, keep_count=5):
        """Keep only the latest N backups"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            print(f"✅ Only {len(backups)} backups found, no cleanup needed")
            return
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x['date'], reverse=True)
        
        # Delete old backups
        deleted_count = 0
        for backup in backups[keep_count:]:
            try:
                os.remove(backup['path'])
                print(f"🗑️ Deleted old backup: {backup['name']}")
                deleted_count += 1
            except:
                print(f"❌ Failed to delete: {backup['name']}")
        
        print(f"✅ Cleanup complete! Deleted {deleted_count} old backups")

def main():
    """Main backup interface"""
    backup_system = AIBackupSystem()
    
    print("🔄 AI Backup System")
    print("=" * 40)
    print("1. Create backup")
    print("2. List backups") 
    print("3. Restore backup")
    print("4. Auto backup")
    print("5. Cleanup old backups")
    print("6. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                name = input("Backup name (or press Enter for auto): ").strip()
                backup_system.create_backup(name if name else None)
                
            elif choice == '2':
                backup_system.list_backups()
                
            elif choice == '3':
                backups = backup_system.list_backups()
                if backups:
                    backup_name = input("Enter backup filename: ").strip()
                    backup_system.restore_backup(backup_name)
                
            elif choice == '4':
                backup_system.auto_backup()
                
            elif choice == '5':
                keep = input("How many backups to keep (default 5): ").strip()
                keep_count = int(keep) if keep.isdigit() else 5
                backup_system.cleanup_old_backups(keep_count)
                
            elif choice == '6':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()