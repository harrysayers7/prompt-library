#!/usr/bin/env python3
"""
Validate all prompts for schema compliance
"""

from pathlib import Path
import frontmatter
import sys

REQUIRED_FIELDS = [
    'name',
    'description', 
    'category',
    'tags',
    'version'
]

RECOMMENDED_FIELDS = [
    'tested_with',
    'performance',
    'use_when',
    'avoid_when'
]

VALID_CATEGORIES = [
    'coding',
    'writing',
    'analysis',
    'design',
    'support',
    'research'
]

VALID_PERFORMANCE = [
    'high',
    'medium', 
    'low',
    'unknown'
]

def validate_prompts():
    prompts_dir = Path('prompts')
    errors = []
    warnings = []
    valid_count = 0
    
    for md_file in prompts_dir.glob('**/*.md'):
        if md_file.name.startswith('_'):
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
            relative_path = md_file.relative_to(prompts_dir)
            
            # Check required fields
            for field in REQUIRED_FIELDS:
                if field not in post.metadata:
                    errors.append(f"{relative_path}: Missing required field '{field}'")
            
            # Check recommended fields
            for field in RECOMMENDED_FIELDS:
                if field not in post.metadata:
                    warnings.append(f"{relative_path}: Missing recommended field '{field}'")
            
            # Validate category
            category = post.metadata.get('category', '')
            if category and category not in VALID_CATEGORIES:
                warnings.append(f"{relative_path}: Unknown category '{category}'")
            
            # Validate performance
            performance = post.metadata.get('performance', '')
            if performance and performance not in VALID_PERFORMANCE:
                warnings.append(f"{relative_path}: Invalid performance value '{performance}'")
            
            # Check content
            if not post.content.strip():
                errors.append(f"{relative_path}: Empty prompt content")
            
            # Check tags format
            tags = post.metadata.get('tags', [])
            if not isinstance(tags, list):
                errors.append(f"{relative_path}: Tags must be a list")
            
            valid_count += 1
            print(f"✓ Valid: {relative_path}")
            
        except Exception as e:
            errors.append(f"{md_file}: Failed to parse - {e}")
    
    # Report results
    print(f"\n📊 Validation Results:")
    print(f"   Valid prompts: {valid_count}")
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"   - {warning}")
    
    if errors:
        print("\n❌ Validation failed! Fix errors before syncing.")
        sys.exit(1)
    else:
        print("\n✅ All prompts valid!")

if __name__ == '__main__':
    validate_prompts()
