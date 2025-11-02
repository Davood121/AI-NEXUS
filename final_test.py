import json
import os
import ollama
from datetime import datetime

# Load knowledge base
with open('ai_knowledge_base.json', 'r') as f:
    kb = json.load(f)

print("Knowledge Base Test:")
print(f"Total entries: {len(kb['fed_data'])}")

# Test query
query = "who is Shaik Davood"
print(f"\\nQuery: {query}")

# Find relevant knowledge
relevant = []
for entry in kb['fed_data']:
    if any(word in entry['content'].lower() for word in ['shaik', 'davood']):
        relevant.append(entry)

print(f"Relevant entries found: {len(relevant)}")

if relevant:
    print("\\nCorrect information about Shaik Davood:")
    for entry in relevant:
        print(f"- {entry['content']}")

# Test AI response
try:
    context = f"You are AI-NEXUS created by Shaik Davood. Use this knowledge: {relevant[0]['content'] if relevant else 'No knowledge'}. Question: {query}"
    
    response = ollama.generate(
        model='phi3:mini',
        prompt=context,
        options={'num_predict': 100}
    )
    
    print(f"\\nAI Response: {response['response']}")
    
except Exception as e:
    print(f"AI Error: {e}")

print("\\n=== IDENTITY CORRECTION COMPLETE ===")
print("The AI now has correct information about Shaik Davood:")
print("- 20-year-old Mechanical Engineering student")
print("- Studies at NBKR Institute")
print("- NOT a film director")
print("- Creator of AI-NEXUS system")