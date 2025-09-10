#!/usr/bin/env python3
"""
Multi-Database Notion Sync - One-way sync from Git to multiple Notion databases
Git is the source of truth. Notion is read-only viewer.
Configured for your specific Notion database structures.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any
import frontmatter
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'harrysayers7/prompt-library')
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main')

if not NOTION_API_KEY:
    print("❌ Missing NOTION_API_KEY in .env file")
    sys.exit(1)

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

# Load database IDs from notion/notion-dev-databases.md
DATABASE_CONFIG_PATH = Path('notion/notion-dev-databases.md')

def load_database_config():
    """Load database IDs from the notion-dev-databases.md file"""
    if not DATABASE_CONFIG_PATH.exists():
        print(f"❌ Database config file not found at {DATABASE_CONFIG_PATH}")
        sys.exit(1)
        
    databases = {}
    current_db = None
    
    with open(DATABASE_CONFIG_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('**Notion Dev Database IDs List:**'):
                continue
                
            # New database entry starts with "**Database Name**"
            if line.startswith('**') and not line.startswith('* **'):
                current_db = line.strip('*').strip()
                databases[current_db] = {}
            
            # Database ID or Data Source ID
            elif line.startswith('* **Database ID'):
                value = line.split('`')[1]
                databases[current_db]['database_id'] = value
            elif line.startswith('* **Data Source ID'):
                value = line.split('`')[1]
                databases[current_db]['data_source_id'] = value
                
    return databases

# Mapping configurations that apply to all databases
CATEGORY_MAP = {
    'coding': 'Technical',
    'writing': 'Writing',
    'analysis': 'Analysis',
    'design': 'Creative',
    'support': 'Communication',
    'research': 'Research',
    'business': 'Business'
}

PERFORMANCE_MAP = {
    'high': 'Excellent',
    'medium': 'Good',
    'low': 'Fair',
    'unknown': 'Needs Work'
}

AI_MODEL_MAP = {
    'gpt-4': 'GPT-4',
    'gpt-3.5': 'GPT-3.5',
    'claude-3': 'Claude',
    'claude-3.5': 'Claude',
    'gemini': 'Gemini'
}

class NotionSync:
    def __init__(self):
        self.prompts_dir = Path('prompts')
        self.code_dir = Path('code')
        self.synced_count = 0
        self.error_count = 0
        self.database_config = load_database_config()
        
    def get_all_prompts(self) -> List[Dict[str, Any]]:
        """Scan directory for all prompt files"""
        prompts = []
        
        for md_file in self.prompts_dir.glob('**/*.md'):
            if md_file.name.startswith('_'):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                # Calculate unique ID from file path
                relative_path = md_file.relative_to(self.prompts_dir)
                prompt_id = str(relative_path).replace('.md', '').replace('\\', '/')
                
                prompt_data = {
                    'id': prompt_id,
                    'path': str(md_file),
                    'github_url': f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/prompts/{relative_path}",
                    'name': post.metadata.get('name', md_file.stem),
                    'description': post.metadata.get('description', ''),
                    'category': post.metadata.get('category', 'uncategorized'),
                    'tags': post.metadata.get('tags', []),
                    'version': post.metadata.get('version', '1.0.0'),
                    'tested_with': post.metadata.get('tested_with', []),
                    'performance': post.metadata.get('performance', 'unknown'),
                    'use_when': post.metadata.get('use_when', ''),
                    'avoid_when': post.metadata.get('avoid_when', ''),
                    'content': post.content,
                    'content_hash': hashlib.md5(post.content.encode()).hexdigest(),
                    'target_db': post.metadata.get('target_db', 'Prompt Library')  # Default to main prompt library
                }
                
                prompts.append(prompt_data)
                print(f"  ✓ Found: {prompt_id}")
                
            except Exception as e:
                print(f"  ✗ Error reading {md_file}: {e}")
                self.error_count += 1
                
        return prompts
    
    def get_existing_pages(self, database_id: str) -> Dict[str, str]:
        """Get all existing pages from a specific Notion database"""
        existing = {}
        
        try:
            response = notion.databases.query(
                database_id=database_id,
                page_size=100
            )
            
            for page in response['results']:
                # Get the prompt name to match
                title_prop = page['properties'].get('Prompt Name', {}) or page['properties'].get('Name', {})
                if title_prop.get('title'):
                    title_text = title_prop['title'][0].get('text', {}).get('content', '')
                    if title_text:
                        existing[title_text] = page['id']
                        
        except Exception as e:
            print(f"  ✗ Error fetching Notion pages: {e}")
            
        return existing
    
    def map_ai_models(self, tested_with: List[str]) -> str:
        """Map tested_with models to Notion AI Model options"""
        for model in tested_with:
            model_lower = model.lower()
            for key, value in AI_MODEL_MAP.items():
                if key in model_lower:
                    return value
        return 'Universal'  # Default if no specific model found
    
    def create_or_update_page(self, prompt: Dict[str, Any], database_id: str, page_id: str = None):
        """Create or update a Notion page for a prompt in the specified database"""
        
        # Map category
        category = CATEGORY_MAP.get(prompt['category'], 'Technical')
        
        # Map performance to effectiveness rating
        effectiveness = PERFORMANCE_MAP.get(prompt['performance'], 'Good')
        
        # Map AI models
        ai_model = self.map_ai_models(prompt['tested_with'])
        
        # Combine use_when and avoid_when for Use Case
        use_case = f"Use when: {prompt['use_when']}\n\nAvoid when: {prompt['avoid_when']}" if prompt['use_when'] or prompt['avoid_when'] else ""
        
        # Add GitHub URL and version to Notes
        notes = f"Version: {prompt['version']}\nGitHub: {prompt['github_url']}"
        
        properties = {
            'Prompt Name': {
                'title': [{'text': {'content': prompt['name']}}]
            },
            'Prompt Text': {
                'rich_text': [{'text': {'content': prompt['content'][:2000]}}]  # Notion limit
            },
            'Description': {
                'rich_text': [{'text': {'content': prompt['description'][:2000]}}]
            },
            'Category': {
                'select': {'name': category}
            },
            'Tags': {
                'multi_select': [{'name': tag} for tag in prompt['tags'][:9]]  # Limit to match your options
            },
            'AI Model': {
                'select': {'name': ai_model}
            },
            'Effectiveness Rating': {
                'select': {'name': effectiveness}
            },
            'Use Case': {
                'rich_text': [{'text': {'content': use_case[:2000]}}]
            },
            'Status': {
                'select': {'name': 'Active'}
            },
            'Notes': {
                'rich_text': [{'text': {'content': notes[:2000]}}]
            },
            'Favorite': {
                'checkbox': prompt['performance'] == 'high'  # Auto-favorite high performance prompts
            }
        }
        
        try:
            if page_id:
                # Update existing page
                notion.pages.update(
                    page_id=page_id,
                    properties=properties
                )
                print(f"    ✓ Updated: {prompt['name']} in {prompt['target_db']}")
            else:
                # Create new page
                notion.pages.create(
                    parent={'database_id': database_id},
                    properties=properties
                )
                print(f"    ✓ Created: {prompt['name']} in {prompt['target_db']}")
                
            self.synced_count += 1
            
        except Exception as e:
            print(f"    ✗ Error syncing {prompt['name']}: {e}")
            self.error_count += 1
    
    def sync(self):
        """Main sync process for all databases"""
        print("\n🚀 Starting Multi-Database Notion Sync...")
        print(f"   Source: Git repository")
        print(f"   Targets: {len(self.database_config)} Notion databases\n")
        
        # Get all prompts from git
        print("📂 Scanning for prompts...")
        prompts = self.get_all_prompts()
        print(f"   Found {len(prompts)} prompts\n")
        
        # Organize prompts by target database
        prompts_by_db = {}
        for prompt in prompts:
            target_db = prompt['target_db']
            if target_db not in prompts_by_db:
                prompts_by_db[target_db] = []
            prompts_by_db[target_db].append(prompt)
        
        # Process each database
        for db_name, db_prompts in prompts_by_db.items():
            if db_name not in self.database_config:
                print(f"⚠️ Warning: Target database '{db_name}' not found in config. Skipping {len(db_prompts)} prompts.")
                continue
                
            db_id = self.database_config[db_name]['database_id']
            print(f"\n📊 Processing database: {db_name} (ID: {db_id})")
            print(f"   Syncing {len(db_prompts)} prompts")
            
            # Get existing Notion pages for this database
            existing_pages = self.get_existing_pages(db_id)
            print(f"   Found {len(existing_pages)} existing pages")
            
            # Sync each prompt to this database
            print(f"   🔄 Syncing prompts to {db_name}...")
            for prompt in db_prompts:
                # Match by name
                page_id = existing_pages.get(prompt['name'])
                self.create_or_update_page(prompt, db_id, page_id)
        
        # Summary
        print(f"\n✅ Sync Complete!")
        print(f"   Synced: {self.synced_count} prompts")
        if self.error_count > 0:
            print(f"   Errors: {self.error_count} (check logs)")
        print(f"\n📝 Remember: Always edit in Git, never in Notion!\n")

if __name__ == '__main__':
    syncer = NotionSync()
    syncer.sync()
