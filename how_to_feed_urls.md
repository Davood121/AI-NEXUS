# How to Feed URLs to Your AI System

## Method 1: Using the AI System Feed Command

When running your AI system (`python ai_system.py`), use this command:

```
feed https://en.wikipedia.org/wiki/Article_(grammar)
```

The AI will automatically:
1. Detect it's a URL (starts with http)
2. Extract content from the webpage
3. Analyze and extract key topics
4. Save to knowledge base with reinforcement learning
5. Search for related information

## Method 2: Direct Script (What we just used)

```python
python simple_url_feed.py
```

## What Happens When You Feed a URL:

1. **Content Extraction**: AI scrapes the webpage and removes HTML/scripts
2. **Text Processing**: Cleans and formats the raw text
3. **Topic Analysis**: Identifies key topics and concepts
4. **Knowledge Storage**: Saves to `ai_knowledge_base.json`
5. **Learning Score**: Increases AI's learning score
6. **Related Search**: Optionally searches for related information

## Current Status:

✅ **Wikipedia Article Successfully Fed!**
- URL: https://en.wikipedia.org/wiki/Article_(grammar)
- Content extracted: 91+ characters
- Key topics identified: grammar-related terms
- Knowledge base entries: 3 total

## Next Steps:

1. Run your AI system: `python ai_system.py`
2. Ask about articles or grammar
3. The AI will use the fed Wikipedia data in responses
4. Feed more URLs using: `feed [URL]`

## Supported URL Types:
- Wikipedia articles
- News websites  
- Blog posts
- Documentation sites
- Any webpage with text content