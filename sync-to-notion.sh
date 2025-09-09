#!/bin/bash
# Quick sync script for manual testing
# Run this from the repository root

echo "🚀 Starting manual Notion sync..."

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

echo "🔄 Running sync..."
python sync/notion-sync.py

echo "✅ Done!"
