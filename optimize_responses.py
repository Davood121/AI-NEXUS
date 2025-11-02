import json

# Optimize AI settings for better responses
settings = {
    "ai_model": "phi3:mini",
    "voice": "en-US-AriaNeural",
    "speech_enabled": True,
    "search_enabled": True,
    "response_length": 180,  # Increased for better detail
    "temperature": 0.6,     # Slightly lower for more focused responses
    "ai_name": "Lambda I-NEXUS",
    "auto_reset": True
}

with open('ai_settings.json', 'w') as f:
    json.dump(settings, f, indent=2)

print("AI response settings optimized!")
print("- Better response length (180 tokens)")
print("- More focused temperature (0.6)")
print("- Cleaner, more informative answers")