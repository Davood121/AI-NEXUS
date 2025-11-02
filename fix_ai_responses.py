import json
import os

# Update AI settings to give cleaner responses
settings = {
    "ai_model": "phi3:mini",
    "voice": "en-US-AriaNeural", 
    "speech_enabled": True,
    "search_enabled": True,
    "response_length": 120,
    "temperature": 0.7,
    "ai_name": "Lambda I-NEXUS",
    "auto_reset": True,
    "mention_creator": False  # New setting to control creator mentions
}

# Save updated settings
with open('ai_settings.json', 'w') as f:
    json.dump(settings, f, indent=2)

print("AI settings updated!")
print("- Responses will be more direct")
print("- Won't mention creator unless asked")
print("- Cleaner, focused answers")