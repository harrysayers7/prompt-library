# LLM Interaction Guide for Prompt Library

This document provides specific instructions for LLMs (like Claude, GPT-4, etc.) on how to interact with, read from, and update this prompt library correctly.

## For LLMs: How to Understand This Repository

As an LLM, when you're asked to interact with this prompt library:

1. **Repository Structure**: Understand that this is a Git-based prompt management system where:
   - All prompts are stored as Markdown files in the `prompts/` directory
   - Each prompt has frontmatter metadata and content
   - Notion integration exists but Git is the source of truth

2. **Reading Prompts**: You can access prompts through:
   - Direct file paths (e.g., `prompts/coding/api-handler.md`)
   - The auto-generated index at `prompts/_index.json`
   - Notion databases (which are read-only views)

3. **Metadata Format**: Each prompt file has standardized frontmatter:
   ```markdown
   ---
   name: "Prompt Name"
   description: "Brief description"
   category: "coding|writing|analysis|etc"
   tags: ["tag1", "tag2"]
   version: "1.0.0"
   tested_with: ["model1", "model2"]
   performance: "high|medium|low"
   use_when: "Usage guidelines"
   avoid_when: "Anti-patterns"
   target_db: "Notion Database Name"
   ---

   # Prompt Content
   ...
   ```

## For LLMs: How to Update This Repository

When asked to create or update prompts in this repository:

1. **Creating New Prompts**:
   - Place files in the correct category folder
   - Use `.md` extension
   - Include ALL required frontmatter fields
   - Ensure the `target_db` field matches a name in `notion/notion-dev-databases.md`

2. **Updating Existing Prompts**:
   - Maintain the existing frontmatter structure
   - Increment version numbers when making significant changes
   - Do not remove existing metadata fields
   - Update `tested_with` if recommending for new models

3. **Committing Changes**:
   - Use clear, descriptive commit messages
   - Commit files to the appropriate locations
   - Remind users that Notion sync is not automatic

4. **Avoid**:
   - Creating prompts without complete frontmatter
   - Modifying the repository structure
   - Suggesting edits directly in Notion
   - Creating prompt files outside the `prompts/` directory

## LLM-Specific Instructions

As an LLM assistant, when helping users with this prompt library:

1. **Always mention sync requirements**: Remind users that changes need to be synced to Notion using:
   ```bash
   ./sync-to-notion.sh
   ```

2. **Frontmatter validation**: When creating prompts, verify that all required fields are present:
   - `name` (string)
   - `description` (string)
   - `category` (string, matching folder)
   - `tags` (array of strings)
   - `version` (string, semantic versioning)
   - `tested_with` (array of strings)
   - `performance` (string: "high", "medium", or "low")
   - `use_when` (string)
   - `avoid_when` (string)
   - `target_db` (string, exact match from notion-dev-databases.md)

3. **Guide on folder structure**: Place new prompts in the appropriate category folders:
   - `prompts/coding/` for development prompts
   - `prompts/writing/` for content generation
   - `prompts/analysis/` for data analysis
   - Other categories as they exist in the repository

4. **Filename conventions**: Use kebab-case for filenames:
   - Good: `api-error-handler.md`
   - Bad: `API Error Handler.md` or `api_error_handler.md`

5. **Target database accuracy**: When creating prompts, carefully match the `target_db` field to one of these database names:
   - "Prompt Library"
   - "Coding Knowledge Database"
   - "AI-Optimized Task Management"
   - "Project Tracker" 
   - "Coding Sub Projects"
   - "AI System Components & Agents"
   - "Cursor Rules Database"
   - *(This list should be kept in sync with notion/notion-dev-databases.md)*

## Example of LLM Creating a New Prompt

When asked to create a new prompt, an LLM should:

1. Identify the appropriate category
2. Create the file in the correct location
3. Include complete frontmatter
4. Provide the prompt content
5. Remind about sync requirements

```markdown
Creating a new prompt at: prompts/coding/react-form-validation.md

---
name: "React Form Validation"
description: "Generates TypeScript code for React form validation using Zod"
category: "coding"
tags: ["react", "typescript", "validation", "zod", "forms"]
version: "1.0.0"
tested_with: ["gpt-4", "claude-3.5"]
performance: "high"
use_when: "Building React forms that need robust validation"
avoid_when: "Simple forms or when not using TypeScript"
target_db: "Coding Knowledge Database"
---

# React Form Validation with Zod

You are an expert React developer specializing in form validation...

[prompt content continues]
```

Then remind the user:
"I've created the prompt file. For it to appear in Notion, you'll need to run the sync script: `./sync-to-notion.sh`"

## Example of LLM Updating an Existing Prompt

When asked to update a prompt, an LLM should:

1. Maintain the existing structure
2. Update only what's needed
3. Increment the version if appropriate
4. Keep all metadata fields

Original:
```markdown
---
name: "API Error Handler"
description: "Error handling for REST APIs"
category: "coding"
tags: ["api", "error-handling"]
version: "1.0.0"
tested_with: ["gpt-4"]
performance: "medium"
use_when: "Building APIs"
avoid_when: "Simple scripts"
target_db: "Coding Knowledge Database"
---

# Basic content...
```

Updated (changes highlighted):
```markdown
---
name: "API Error Handler"
description: "Comprehensive error handling for REST APIs with TypeScript" # Updated
category: "coding"
tags: ["api", "error-handling", "typescript"] # Added tag
version: "1.1.0" # Incremented version
tested_with: ["gpt-4", "claude-3.5"] # Added model
performance: "high" # Improved rating
use_when: "Building production-grade REST APIs with TypeScript"
avoid_when: "Simple scripts or prototypes"
target_db: "Coding Knowledge Database" # Maintained
---

# Enhanced content...
```

Then remind the user about syncing:
"I've updated the prompt file. Remember to run `./sync-to-notion.sh` to sync these changes to Notion."
