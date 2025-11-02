import json
import os
from datetime import datetime

# Create knowledge base entry directly
identity_data = {
    'timestamp': datetime.now().isoformat(),
    'content': 'Shaik Davood is a 20-year-old Mechanical Engineering student (2nd year) at NBKR Institute of Science and Technology, Vidyanagar. Born November 5, 2003. Skills: Python, AI, OpenCV, Flask, Raspberry Pi, Android Studio. Projects: Echo AI, AAI Agent, Custom Pi OS, TESLAGUARD, Lambda I-NEXUS. NOT a film director or Tamil cinema person.',
    'analysis': {
        'key_topics': ['shaik', 'davood', 'mechanical', 'engineering', 'student', 'nbkr', 'python', 'projects'],
        'word_count': 45,
        'summary': 'Shaik Davood creator information - mechanical engineering student and AI developer'
    },
    'related_searches': [],
    'reinforcement_score': 2.0,
    'usage_count': 0
}

# Load or create knowledge base
try:
    if os.path.exists('ai_knowledge_base.json'):
        with open('ai_knowledge_base.json', 'r') as f:
            kb = json.load(f)
    else:
        kb = {'fed_data': [], 'learned_concepts': {}, 'reinforcement_scores': {}}
except:
    kb = {'fed_data': [], 'learned_concepts': {}, 'reinforcement_scores': {}}

# Add identity data
kb['fed_data'].append(identity_data)

# Update learned concepts
for topic in identity_data['analysis']['key_topics']:
    kb['learned_concepts'][topic] = kb['learned_concepts'].get(topic, 0) + 1

# Save knowledge base
with open('ai_knowledge_base.json', 'w') as f:
    json.dump(kb, f, indent=2)

print("Identity information fed successfully!")
print("AI now has correct information about Shaik Davood")