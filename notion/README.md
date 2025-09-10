# Notion Integration

This folder contains configuration and scripts for integrating your prompt library with Notion databases.

## Database IDs

The file `notion-dev-databases.md` contains all the database IDs and data source IDs needed for syncing with Notion. These IDs are used by the sync scripts to connect to the correct Notion databases.

### Database Configuration

The sync system reads these IDs from the `notion-dev-databases.md` file and uses them to sync content from your Git repository to the corresponding Notion databases. This allows you to maintain a single source of truth in Git while having the content available for viewing and reference in Notion.

## How Syncing Works

1. The `sync-to-notion.sh` script in the repository root calls the `sync/multi-db-notion-sync.py` script
2. The Python script reads the database IDs from `notion-dev-databases.md`
3. It then scans the `prompts/` directory for markdown files
4. Each prompt file can specify which database it should be synced to using the `target_db` front matter field
5. The script creates or updates the corresponding entries in each Notion database

## Adding a New Database

To add a new Notion database to the sync system:

1. Create a new database in Notion with the appropriate structure
2. Add the database ID and data source ID to `notion-dev-databases.md`
3. The sync system will automatically recognize and use the new database

## Automated Syncing

You can set up automated syncing by using the pre-commit hook:

```bash
cp scripts/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This will automatically run the sync script whenever you commit changes to prompt files or Notion configuration.
