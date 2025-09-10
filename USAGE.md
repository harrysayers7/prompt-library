# Prompt Library Usage Guide

This comprehensive guide explains how to use the entire prompt library system, including adding new prompts, organization, sync features, and best practices.

## Overview

The prompt library is a Git-based system for managing, versioning, and sharing prompts for AI models. It maintains Git as the source of truth while offering Notion integration for easy browsing and sharing.

## Repository Structure

```
prompt-library/
├── prompts/              # All prompt content
│   ├── coding/           # Technical prompts
│   ├── writing/          # Content generation prompts
│   ├── analysis/         # Data analysis prompts
│   └── _index.json       # Auto-generated index for LLMs
│
├── notion/               # Notion integration
│   ├── notion-dev-databases.md  # Database IDs
│   ├── README.md         # Integration documentation
│   └── USAGE.md          # Notion usage instructions
│
├── sync/                 # Sync scripts
│   ├── notion-sync.py             # Original single-DB sync
│   ├── multi-db-notion-sync.py    # Multi-database sync
│   └── generate-index.py          # Creates _index.json
│
├── scripts/              # Utility scripts
│   └── pre-commit.sample # Git hook template
│
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
├── sync-to-notion.sh     # Main sync script
└── README.md             # Main documentation
```

## Adding New Prompts

### 1. Creating a New Prompt File

Create a Markdown file in the appropriate category folder under `prompts/`:

```bash
# Example for creating a new coding prompt
touch prompts/coding/react-component-generator.md
```

### 2. Adding Content with Frontmatter

Each prompt file needs frontmatter metadata and the actual prompt content:

```markdown
---
name: "React Component Generator"
description: "Creates well-structured React components with proper TypeScript typing"
category: "coding"
tags: ["react", "typescript", "frontend"]
version: "1.0.0"
tested_with: ["gpt-4", "claude-3.5"]
performance: "high"
use_when: "Building complex React applications with TypeScript"
avoid_when: "Simple components or JavaScript-only projects"
target_db: "Coding Knowledge Database"
---

# React Component Generator

I want you to create a professional-grade React component that follows best practices for production code.

## Requirements:
1. Use TypeScript with proper typing
2. Include proper prop validation
3. Follow the functional component pattern with hooks
4. Include documentation comments

[Additional prompt content...]
```

### 3. Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Display name of the prompt | `"API Error Handler"` |
| `description` | Brief description | `"Generates error handling code"` |
| `category` | Main category | `"coding"` (matches folder structure) |
| `tags` | Array of tags | `["api", "error-handling"]` |
| `version` | Semantic version | `"1.0.0"` |
| `tested_with` | Models tested with | `["gpt-4", "claude-3"]` |
| `performance` | Quality rating | `"high"`, `"medium"`, or `"low"` |
| `use_when` | Usage guidelines | `"Building production APIs"` |
| `avoid_when` | Anti-patterns | `"Quick prototypes"` |
| `target_db` | Notion database to sync to | `"Prompt Library"` |

## Ways to Edit Prompts

### 1. Local Git Workflow (Recommended)

```bash
# Clone the repository
git clone https://github.com/harrysayers7/prompt-library.git
cd prompt-library

# Create .env file
cp .env.example .env
# Add your NOTION_API_KEY

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hook (optional)
cp scripts/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Make your changes...

# Commit and push
git add .
git commit -m "Add new prompt for React components"
git push
```

### 2. GitHub Web Interface

1. Navigate to the repository on GitHub
2. Browse to the file you want to edit (or create a new file)
3. Use the edit button (pencil icon) or "Add file" button
4. Make your changes
5. Commit directly to the main branch
6. **Note:** Notion sync will not happen automatically - you'll need to run sync manually

### 3. Using Claude

1. Ask Claude to create or modify files in your repository
2. Claude will commit the changes to GitHub
3. **Note:** Notion sync will not happen automatically - you'll need to run sync manually

## Running the Sync

The sync process pushes content from Git to Notion (one-way sync).

### Manual Sync

```bash
# From repository root
./sync-to-notion.sh
```

### Automated Sync Options

1. **Git Pre-commit Hook**: Automatically syncs when you commit changes locally
   ```bash
   cp scripts/pre-commit.sample .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. **GitHub Actions**: Automatically syncs when you push to the main branch
   - See instructions in `notion/USAGE.md` for setting up GitHub Actions

## Is It Live Synced?

**No, the repository is not live synced by default.** 

- Changes in Git do not automatically appear in Notion without running a sync
- You must either run the sync script manually or set up automation
- Notion is read-only - changes made in Notion will be overwritten by the next sync

## Using Prompts in Your Applications

### Direct File Access

```python
import json

# Load all prompts
with open('prompts/_index.json') as f:
    prompts = json.load(f)

# Get specific prompt
prompt = next(p for p in prompts['prompts'] if p['id'] == 'coding/api-error-handler')

# Use the prompt
print(prompt['content'])
```

### Via GitHub API

```python
import requests

# Raw file from GitHub
response = requests.get(
    'https://raw.githubusercontent.com/harrysayers7/prompt-library/main/prompts/_index.json'
)
prompts = response.json()

# Find and use a prompt
prompt = next(p for p in prompts['prompts'] if p['id'] == 'coding/api-error-handler')
```

### Via Notion (Read-Only)

1. Open the appropriate Notion database
2. Browse and search for prompts
3. Copy the prompt content when needed
4. **Remember:** Do not edit in Notion, as changes will be overwritten

## Maintaining the Repository

### Updating the Index

If you've made changes and want to regenerate the index:

```bash
python sync/generate-index.py
```

### Validating Prompts

To check for any issues with prompt formatting:

```bash
python sync/validate.py
```

### Adding a New Category

1. Create a new folder under `prompts/`
2. Add an entry to the category mapping in sync scripts if needed
3. Begin adding prompts to the new category

### Adding a New Notion Database

1. Create the database in Notion
2. Add its ID to `notion/notion-dev-databases.md`
3. Use the database name as `target_db` in prompt frontmatter

## Best Practices

1. **Git is Truth**: Always edit in Git, never in Notion
2. **Consistent Structure**: Follow the frontmatter schema precisely
3. **Test Before Committing**: Ensure prompts are formatted correctly
4. **One Prompt Per File**: Keep each prompt in its own file
5. **Descriptive Names**: Use clear, descriptive filenames
6. **Version Control**: Use semantic versioning for prompt versions
7. **Documentation**: Include clear usage guidelines in each prompt
8. **Organization**: Use the correct category folder for each prompt

## Troubleshooting

### Sync Issues

- Check your `.env` file for correct API keys
- Ensure your Notion integration has access to all databases
- Look for error messages in the sync script output

### Missing Prompts in Notion

- Verify the `target_db` field matches a database name exactly
- Run the sync script manually to check for errors
- Ensure the prompt file has correct frontmatter format

### Prompt Not Working

- Check the prompt format and structure
- Verify the tested_with field matches your usage
- Consider updating the version and testing with newer models

## Security Considerations

- Never commit API keys or sensitive information to the repository
- Use `.env` for local configuration
- Use GitHub Secrets for CI/CD configuration

## Additional Resources

- [Notion API Documentation](https://developers.notion.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Markdown Guide](https://www.markdownguide.org/)
- [Effective Prompt Engineering Techniques](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)
