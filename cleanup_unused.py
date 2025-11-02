import os
import shutil

def cleanup_unused_files():
    """Remove unused files while keeping core workflow"""
    
    # Files safe to remove (duplicates, tests, temp files)
    files_to_remove = [
        # Duplicate/test AI systems
        'ai_with_edge_tts.py',
        'ai_with_offline_tts.py', 
        'ai_with_piper_tts.py',
        'clean_ai_system.py',
        'customizable_ai.py',
        'final_test.py',
        'simple_ai.py',
        'simple_feed.py',
        'simple_run.py',
        'simple_text_ai.py',
        'simple_url_feed.py',
        'simple_working_ai.py',
        'text_only_ai.py',
        'updated_ai_system.py',
        'working_ai.py',
        'run_ai.py',
        
        # Temporary speech files
        'temp_speech_1762039851.mp3',
        'temp_speech_1762040003.mp3',
        'temp_speech.mp3',
        'test_edge_neural.mp3',
        
        # Setup/fix scripts (one-time use)
        'correct_identity.py',
        'feed_correct_identity.py',
        'feed_identity.py',
        'feed_url_command.py',
        'feed_url.py',
        'fix_ai_responses.py',
        'fix_all_names.py',
        'optimize_responses.py',
        'setup_edge_tts.py',
        'setup_piper.py',
        'setup_updated.py',
        'setup.py',
        'test_identity.py',
        'update_all.py',
        'update_name.py',
        
        # Extra batch files
        'run_system.bat',
        'run.bat',
        
        # Extra requirements
        'requirements_offline.txt',
        'requirements_piper.txt',
        
        # Duplicate knowledge files
        'ai_knowledge.json',
        'ai_memory.json',
        
        # Extra documentation
        'README_UPDATED.md',
        'how_to_feed_urls.md',
        'creator_info.txt'
    ]
    
    print("🧹 Cleaning up unused files...")
    removed_count = 0
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")
    
    print(f"\n🎉 Cleanup complete! Removed {removed_count} unused files.")
    print("\n📁 Core files preserved:")
    print("- ai_system.py (main system)")
    print("- ai_system_fixed.py (fixed version)")
    print("- stable_ai.py (stable version)")
    print("- ai_settings.json (settings)")
    print("- ai_knowledge_base.json (knowledge)")
    print("- requirements.txt & requirements_fixed.txt")
    print("- backup_system.py & quick_backup.py")
    print("- frontend/ folder")
    print("- ai_backups/ folder")

if __name__ == "__main__":
    cleanup_unused_files()
    input("\nPress Enter to continue...")