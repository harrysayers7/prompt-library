#!/usr/bin/env python3
"""
Notion Sync - One-way sync from Git to Notion
Git is the source of truth. Notion is read-only viewer.
Configured for your specific Notion database structure.
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
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID', '2bedbdf10e314b638e3fc21d7aa8b373')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'harrysayers7/prompt-library')
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main')

if not NOTION_API_KEY:
    print("❌ Missing NOTION_API_KEY in .env file")
    sys.exit(1)

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

# Mapping configurations for your database
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
        self.synced_count = 0
        self.error_count = 0
        
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
                    'content_hash': hashlib.md5(post.content.encode()).hexdigest()
                }
                
                prompts.append(prompt_data)
                print(f"  ✓ Found: {prompt_id}")
                
            except Exception as e:
                print(f"  ✗ Error reading {md_file}: {e}")
                self.error_count += 1
                
        return prompts
    
    def get_existing_pages(self) -> Dict[str, str]:
        """Get all existing pages from Notion database"""
        existing = {}
        
        try:
            response = notion.databases.query(
                database_id=NOTION_DATABASE_ID,
                page_size=100
            )
            
            for page in response['results']:
                # Get the prompt name to match
                title_prop = page['properties'].get('Prompt Name', {})
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
    
    def create_or_update_page(self, prompt: Dict[str, Any], page_id: str = None):
        """Create or update a Notion page for a prompt"""
        
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
                print(f"    ✓ Updated: {prompt['name']}")
            else:
                # Create new page
                notion.pages.create(
                    parent={'database_id': NOTION_DATABASE_ID},
                    properties=properties
                )
                print(f"    ✓ Created: {prompt['name']}")
                
            self.synced_count += 1
            
        except Exception as e:
            print(f"    ✗ Error syncing {prompt['name']}: {e}")
            self.error_count += 1
    
    def sync(self):
        """Main sync process"""
        print("\n🚀 Starting Notion Sync...")
        print(f"   Source: Git repository")
        print(f"   Target: Notion database (ID: {NOTION_DATABASE_ID})\n")
        
        # Get all prompts from git
        print("📂 Scanning for prompts...")
        prompts = self.get_all_prompts()
        print(f"   Found {len(prompts)} prompts\n")
        
        # Get existing Notion pages
        print("📊 Fetching existing Notion pages...")
        existing_pages = self.get_existing_pages()
        print(f"   Found {len(existing_pages)} existing pages\n")
        
        # Sync each prompt
        print("🔄 Syncing prompts to Notion...")
        for prompt in prompts:
            # Match by name
            page_id = existing_pages.get(prompt['name'])
            self.create_or_update_page(prompt, page_id)
        
        # Summary
        print(f"\n✅ Sync Complete!")
        print(f"   Synced: {self.synced_count} prompts")
        if self.error_count > 0:
            print(f"   Errors: {self.error_count} (check logs)")
        print(f"\n📝 Remember: Always edit in Git, never in Notion!\n")

if __name__ == '__main__':
    syncer = NotionSync()
    syncer.sync()
