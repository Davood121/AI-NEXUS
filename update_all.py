import os

# Files to update
files_to_update = [
    'ai_system.py',
    'customizable_ai.py', 
    'ai_with_edge_tts.py',
    'ai_with_offline_tts.py',
    'simple_text_ai.py',
    'setup.py'
]

for filename in files_to_update:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace all occurrences
        content = content.replace('"ΛI-NEXUSd AI"', '"ΛI-NEXUS"')
        content = content.replace("'ΛI-NEXUSd AI'", "'ΛI-NEXUS'")
        content = content.replace('ΛI-NEXUSd AI', 'ΛI-NEXUS')
        content = content.replace('ΛI-NEXUS', 'ΛI-NEXUS')
        content = content.replace('REVOLUTIONARY AI SYSTEM', 'REVOLUTIONARY AI SYSTEM')
        content = content.replace('Revolutionary AI System', 'Revolutionary AI System')
        content = content.replace("I'm ΛI-NEXUS, your", "I'm ΛI-NEXUS, your")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {filename}")
    else:
        print(f"⚠️ {filename} not found")

print("\n🎉 All files updated to ΛI-NEXUS branding!")