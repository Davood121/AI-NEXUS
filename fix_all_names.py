import os
import glob

# Get all Python files
python_files = glob.glob("*.py")

for filename in python_files:
    if filename == "fix_all_names.py":  # Skip this script
        continue
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace all variations
        replacements = [
            ('DAVOO', 'ΛI-NEXUS'),
            ('davoo', 'ΛI-NEXUS'),
            ('Davoo', 'ΛI-NEXUS'),
            ('"Davood AI"', '"ΛI-NEXUS"'),
            ("'Davood AI'", "'ΛI-NEXUS'"),
            ('Davood AI', 'ΛI-NEXUS'),
            ('DEFAULT AI SYSTEM', 'REVOLUTIONARY AI SYSTEM'),
            ('Default AI System', 'Revolutionary AI System'),
            ("I'm your", "I'm ΛI-NEXUS, your"),
            ("Hello! I'm {self.settings['ai_name']}", "Hello! I'm ΛI-NEXUS")
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {filename}")
        
    except Exception as e:
        print(f"❌ Error with {filename}: {e}")

print("\n🎉 All files updated to ΛI-NEXUS!")