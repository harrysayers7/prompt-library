# Prompt Library

> Production-ready prompt management system with Notion sync. Git is the source of truth.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/harrysayers7/prompt-library.git
cd prompt-library

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your NOTION_API_KEY and NOTION_DATABASE_ID

# Test local sync
python sync/notion-sync.py
```

## Philosophy

**Ship Factor: 9/10** - This is the boring solution that works.

- Git is the single source of truth
- Notion is a read-only viewer
- No sync conflicts, no debugging complex state
- LLMs read directly from git (fast, no API limits)

## Structure

```
prompts/
├── coding/          # Technical prompts
├── writing/         # Content generation
├── analysis/        # Data analysis & review
└── _index.json     # Auto-generated for LLM consumption
```

## Adding a New Prompt

1. Create a new `.md` file in the appropriate category folder
2. Add frontmatter with metadata
3. Write your prompt
4. Commit and push - GitHub Actions handles the rest

### Example Prompt

```markdown
---
name: "API Error Handler"
description: "Generates comprehensive error handling for REST APIs"
category: "coding"
tags: ["api", "error-handling", "rest"]
version: "1.0.0"
tested_with: ["gpt-4", "claude-3"]
performance: "high"
use_when: "Building production APIs"
avoid_when: "Quick prototypes"
---

# Context
You are an expert backend engineer...

# Task
Generate error handling code that...
```

## LLM Integration

### Direct File Access (Fastest)
```python
import json

# Load all prompts
with open('prompts/_index.json') as f:
    prompts = json.load(f)

# Get specific prompt
prompt = next(p for p in prompts['prompts'] if p['id'] == 'coding/api-error-handler')
```

### Via API
```python
import requests

# Raw file from GitHub
response = requests.get(
    'https://raw.githubusercontent.com/harrysayers7/prompt-library/main/prompts/_index.json'
)
prompts = response.json()
```

## Notion Setup

1. Create a Notion database with these properties:
   - Name (title)
   - Description (text)
   - Category (select)
   - Tags (multi-select)
   - Version (text)
   - Performance (select)
   - Use When (text)
   - Avoid When (text)
   - Content (text)
   - GitHub URL (url)

2. Get your API key: https://www.notion.so/my-integrations
3. Share the database with your integration
4. Add credentials to GitHub Secrets:
   - `NOTION_API_KEY`
   - `NOTION_DATABASE_ID`

## Maintenance

### Update Index Manually
```bash
python sync/generate-index.py
```

### Force Notion Sync
```bash
python sync/notion-sync.py --force
```

### Validate Prompts
```bash
python sync/validate.py
```

## Upgrade Path

**Don't build these until you need them:**

- **Hit rate limits?** → Add caching layer
- **Need search?** → Add embeddings to index.json
- **Multiple editors?** → Add PR workflow
- **Need versioning?** → Use git tags

## Contributing

1. Edit prompts only in git (never in Notion)
2. Follow the frontmatter schema
3. Test locally before pushing
4. One prompt per file

## Why This Design?

- **No sync conflicts**: One-way sync eliminates complexity
- **Fast LLM access**: Direct file reads, no API overhead
- **Version control**: Git tracks everything properly
- **Simple to maintain**: One Python script, clear flow
- **Scales well**: Add folders/categories as needed

---

**Remember: The boring solution ships. The clever solution becomes technical debt.**