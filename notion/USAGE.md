# Using the Prompt Library Notion Sync System

This document provides detailed instructions on how to use the Notion sync system for your prompt library in different scenarios.

## Overview

The Notion sync system maintains your Git repository as the source of truth and syncs content to your Notion databases for easy reference and sharing. **It's important to understand that this is a one-way sync: Git → Notion**. Changes made in Notion will not be synced back to Git and will be overwritten on the next sync.

## Sync Status

- **Not Live Synced**: The sync is not automatic/live. It requires you to trigger it either manually or through a Git hook.
- **Manual Trigger Required**: You need to run the sync script or commit changes (if using the pre-commit hook) to update Notion.

## Usage Scenarios

### 1. Editing Files Directly in GitHub UI

If you edit files directly in the GitHub web interface:

1. Make your changes and commit them
2. The changes will NOT automatically sync to Notion
3. You'll need to manually trigger a sync by:
   - Pulling the changes to your local repository: `git pull`
   - Running the sync script: `./sync-to-notion.sh`

### 2. Using Claude to Make Changes

When using Claude to add or edit files:

1. Ask Claude to create or modify files in your repository
2. Claude will commit the changes to GitHub
3. Similar to editing in GitHub UI, you'll need to manually sync:
   - Pull the changes locally: `git pull`
   - Run the sync script: `./sync-to-notion.sh`

### 3. Working Locally with Git

For local development:

1. Clone the repository: `git clone https://github.com/harrysayers7/prompt-library.git`
2. Make your changes locally
3. Set up the pre-commit hook for automatic sync on commit:
   ```bash
   cp scripts/pre-commit.sample .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```
4. When you commit changes, the pre-commit hook will automatically run the sync
5. If you don't want to use the pre-commit hook, manually run: `./sync-to-notion.sh`

## Adding Content with Proper Front Matter

For your content to sync correctly to the right Notion database, include proper front matter:

```markdown
---
name: "My Awesome Prompt"
description: "A prompt that does amazing things"
category: "coding"
tags: ["gpt-4", "python", "data-analysis"]
version: "1.0.0"
tested_with: ["claude-3.5", "gpt-4"]
performance: "high"
use_when: "You need to analyze complex data structures"
avoid_when: "Simple text formatting is all you need"
target_db: "Prompt Library"  # Specify which Notion DB to sync to
---

# My Awesome Prompt

Your prompt content goes here...
```

The `target_db` field is crucial - it must exactly match one of the database names in `notion/notion-dev-databases.md`.

## Setup Requirements

1. **Environment Variables**: Create a `.env` file based on `.env.example` with your Notion API key.
2. **Python Dependencies**: Install dependencies with `pip install -r requirements.txt` (the sync script will do this for you).
3. **Notion Integration**: You must have a Notion integration with access to all the databases.

## Common Issues and Troubleshooting

- **Authentication Errors**: Ensure your Notion API key is correct and the integration has access to all databases.
- **Database Not Found**: Make sure the `target_db` in the front matter exactly matches a database name in `notion-dev-databases.md`.
- **Sync Script Fails**: Check that Python 3.6+ is installed and all dependencies are installed.
- **Changes Not Appearing in Notion**: Make sure you've run the sync script after making changes.

## Setting Up GitHub Actions for Automated Sync (Optional)

For fully automated syncing, you can set up a GitHub Action:

1. Create a file `.github/workflows/notion-sync.yml`:
   ```yaml
   name: Sync to Notion

   on:
     push:
       branches: [main]
       paths:
         - 'prompts/**'
         - 'notion/**'

   jobs:
     sync:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
         - name: Run sync script
           run: ./sync-to-notion.sh
           env:
             NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
   ```

2. Add your `NOTION_API_KEY` as a repository secret in GitHub.

This will automatically sync changes to Notion whenever you push to the main branch.

## Best Practices

1. **Always Edit in Git**: Never make changes directly in Notion, as they'll be overwritten.
2. **Commit Often**: Smaller, more frequent commits make tracking changes easier.
3. **Use Descriptive Commit Messages**: This helps track what was changed and why.
4. **Verify Syncs**: Check Notion after syncing to ensure everything appears correctly.

## Additional Resources

- Notion API Documentation: https://developers.notion.com/
- Python Notion Client: https://github.com/ramnes/notion-sdk-py
