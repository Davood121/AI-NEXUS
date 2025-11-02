import re

# Read the file
with open('ai_system.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences
content = content.replace('"ΛI-NEXUSd AI"', '"ΛI-NEXUS"')
content = content.replace("'ΛI-NEXUSd AI'", "'ΛI-NEXUS'")
content = content.replace('REVOLUTIONARY AI SYSTEM', 'REVOLUTIONARY AI SYSTEM')

# Write back
with open('ai_system.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AI name updated to ΛI-NEXUS")