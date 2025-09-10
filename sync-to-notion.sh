#!/bin/bash
# Prompt Library Sync Script for Notion Integration
# Syncs content from this repo to multiple Notion databases
# Run this from the repository root

echo "🚀 Starting Notion database sync..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Creating .env file template..."
    cp .env.example .env
    echo "Please edit .env and add your NOTION_API_KEY"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check if the notion-dev-databases.md file exists
if [ ! -f "notion/notion-dev-databases.md" ]; then
    echo "❌ notion/notion-dev-databases.md not found!"
    echo "Please make sure the file exists with the proper database IDs."
    exit 1
fi

echo "🔄 Running multi-database sync..."
python sync/multi-db-notion-sync.py

# If the script was run from GitHub Actions
if [ "$CI" = "true" ]; then
    echo "✅ CI sync complete!"
else
    echo "✅ Local sync complete!"
    echo ""
    echo "💡 TIP: You can add this as a git pre-commit hook to auto-sync on commit"
    echo "    cp scripts/pre-commit.sample .git/hooks/pre-commit"
    echo "    chmod +x .git/hooks/pre-commit"
fi
