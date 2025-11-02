import os
import shutil

def cleanup_project():
    """Remove unwanted files and keep only essential ones"""
    print("🧹 Cleaning up AI project...")
    
    # Essential files to keep
    keep_files = {
        # Main AI systems
        'customizable_ai.py',           # Best - fully customizable
        'ai_with_offline_tts.py',       # Offline speech version
        'simple_text_ai.py',           # Text-only reliable version
        
        # Setup and requirements
        'requirements_offline.txt',     # Dependencies for offline TTS
        'setup_updated.py',            # Setup script
        
        # Documentation
        'README_UPDATED.md',           # Main documentation
        
        # Backup system
        'backup_system.py',            # Backup functionality
        'quick_backup.py',             # Quick backup
        
        # Generated files (keep if they exist)
        'ai_settings.json',            # User settings
        'ai_knowledge.json',           # AI knowledge base
        'ai_memory.json',              # AI memory
    }
    
    # Files to definitely remove (old/broken versions)
    remove_files = {
        'ai_system.py',                # Old version
        'text_ai_system.py',           # Duplicate
        'fast_ai_system.py',           # Old version
        'ultra_fast_ai.py',            # Old version
        'lightning_ai.py',             # Old version
        'gpu_ai_system.py',            # Had issues
        'force_gpu_ai.py',             # Had issues
        'final_ai.py',                 # Old version
        'conscious_ai_system.py',      # Complex version
        'realtime_ai_system.py',       # Old version
        'ultimate_ai_system.py',       # Too complex
        'working_voice_ai.py',         # Old version
        'guaranteed_voice_ai.py',      # Old version
        'voice_fix_ai.py',             # Old version
        'ai_with_speech.py',           # Had connection issues
        'ai_with_fallback_speech.py',  # Complex version
        'final_working_ai.py',         # Had SAPI issues
        'force_voice_ai.py',           # Old version
        'ai_with_external_tts.py',     # Complex version
        'clean_tts_ai.py',             # Old version
        
        # Test files
        'test_voice.py',               # Test file
        'test_voice_only.py',          # Test file
        'simple_voice_test.py',        # Test file
        'tts_options_test.py',         # Test file
        'system_checker.py',           # Test file
        'gpu_check.py',                # Test file
        
        # Old requirements
        'requirements.txt',            # Old requirements
        'simple_requirements.txt',     # Old requirements
        'requirements_with_speech.txt', # Old requirements
        'requirements_fallback.txt',   # Old requirements
        'requirements_text_only.txt',  # Old requirements
        
        # Old setup files
        'setup.py',                    # Old setup
        
        # Batch files
        'enable_gpu.bat',              # Old batch file
        'run_ultimate_ai.bat',         # Old batch file
        
        # Old documentation
        'README.md',                   # Old readme
    }
    
    # Get all files in directory
    all_files = set(os.listdir('.'))
    
    # Files to remove (in remove_files list and exist)
    files_to_remove = remove_files.intersection(all_files)
    
    # Remove unwanted files
    removed_count = 0
    for file in files_to_remove:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"🗑️ Removed: {file}")
                removed_count += 1
            elif os.path.isdir(file):
                shutil.rmtree(file)
                print(f"🗑️ Removed directory: {file}")
                removed_count += 1
        except Exception as e:
            print(f"❌ Could not remove {file}: {e}")
    
    # Show what's kept
    remaining_files = set(os.listdir('.'))
    essential_files = keep_files.intersection(remaining_files)
    
    print(f"\n✅ Cleanup complete!")
    print(f"🗑️ Removed {removed_count} unwanted files")
    print(f"📁 Kept {len(essential_files)} essential files")
    
    print(f"\n📋 Essential files kept:")
    for file in sorted(essential_files):
        print(f"  ✅ {file}")
    
    # Show other files (not in keep list but not removed)
    other_files = remaining_files - keep_files - {'.', '..', 'cleanup_project.py'}
    if other_files:
        print(f"\n📋 Other files (review manually):")
        for file in sorted(other_files):
            if not file.startswith('.'):  # Skip hidden files
                print(f"  ❓ {file}")
    
    print(f"\n🎯 Recommended main files to use:")
    print(f"  🌟 customizable_ai.py - Best option (fully customizable)")
    print(f"  🔊 ai_with_offline_tts.py - Offline speech version")
    print(f"  📝 simple_text_ai.py - Text-only reliable version")

if __name__ == "__main__":
    cleanup_project()