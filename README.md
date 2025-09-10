# Prompt Library

> Production-ready prompt management system with multi-database Notion sync. Git is the source of truth.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/harrysayers7/prompt-library.git
cd prompt-library

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your NOTION_API_KEY

# Test local sync to all Notion databases
./sync-to-notion.sh
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

notion/
├── notion-dev-databases.md  # Database IDs for all Notion databases
├── README.md                # Documentation about Notion integration
└── USAGE.md                 # Detailed usage instructions
```

## Adding a New Prompt

1. Create a new `.md` file in the appropriate category folder
2. Add frontmatter with metadata (including target_db for Notion sync)
3. Write your prompt
4. Commit and push - GitHub Actions or local hooks handle the sync

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
target_db: "Coding Knowledge Database"  # Which Notion DB to sync to
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

## Notion Integration

The system now supports syncing to multiple Notion databases:

1. **Database Configuration**: 
   - All database IDs are stored in `notion/notion-dev-databases.md`
   - Each prompt specifies which database to sync to using the `target_db` frontmatter field

2. **Multiple Database Support**:
   - Prompts can be directed to different databases based on their purpose
   - Code prompts go to coding databases, tasks to project management, etc.

3. **Usage Instructions**:
   - See `notion/USAGE.md` for detailed instructions on using the Notion sync system
   - See `notion/README.md` for information about the Notion integration

4. **Setup Requirements**:
   - Create a Notion integration: https://www.notion.so/my-integrations
   - Share all databases with your integration
   - Add your NOTION_API_KEY to .env or GitHub Secrets

## Maintenance

### Sync to Notion
```bash
./sync-to-notion.sh
```

### Update Index Manually
```bash
python sync/generate-index.py
```

### Validate Prompts
```bash
python sync/validate.py
```

## Automation Options

1. **Pre-commit Hook** (Local):
   ```bash
   cp scripts/pre-commit.sample .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. **GitHub Actions** (CI/CD):
   - Set up a workflow to run the sync script on push
   - See `notion/USAGE.md` for setup instructions

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
5. Specify the target Notion database in frontmatter

## Why This Design?

- **No sync conflicts**: One-way sync eliminates complexity
- **Fast LLM access**: Direct file reads, no API overhead
- **Version control**: Git tracks everything properly
- **Simple to maintain**: One Python script, clear flow
- **Scales well**: Add folders/categories and databases as needed
- **Flexible organization**: Sync different prompts to different Notion databases

---

**Remember: The boring solution ships. The clever solution becomes technical debt.**