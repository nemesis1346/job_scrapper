#!/usr/bin/env python3
"""
Debug script for GitHub Issues Creator
This script helps diagnose issues with GitHub API access
"""

import os
import sys
import requests
from typing import Optional

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

def test_github_connection(token: str) -> bool:
    """Test GitHub API connection."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub connection successful!")
            print(f"   Authenticated as: {user_data.get('login', 'Unknown')}")
            print(f"   User ID: {user_data.get('id', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_repository_access(token: str, repo: str) -> bool:
    """Test repository access."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Repository access successful!")
            print(f"   Repository: {repo_data.get('full_name', repo)}")
            print(f"   Description: {repo_data.get('description', 'No description')}")
            print(f"   Private: {repo_data.get('private', 'Unknown')}")
            print(f"   Issues enabled: {repo_data.get('has_issues', 'Unknown')}")
            return True
        else:
            print(f"❌ Repository access failed: {response.status_code}")
            print(f"   URL: {url}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Repository access error: {e}")
        return False

def test_create_label(token: str, repo: str) -> bool:
    """Test creating a label."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.github.com/repos/{repo}/labels"
    test_label = {
        "name": "test-label",
        "color": "ff0000",
        "description": "Test label for debugging"
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_label)
        if response.status_code == 201:
            print(f"✅ Label creation successful!")
            return True
        elif response.status_code == 422:
            print(f"⚠️  Label already exists (this is OK)")
            return True
        else:
            print(f"❌ Label creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Label creation error: {e}")
        return False

def main():
    """Main debug function."""
    print("🔍 GitHub Issues Creator Debug Tool")
    print("=" * 40)
    
    # Get environment variables
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    print(f"📋 Environment Variables:")
    print(f"   GITHUB_TOKEN: {'✅ Set' if token else '❌ Not set'}")
    if token:
        print(f"   Token preview: {token[:10]}...")
    
    print(f"   GITHUB_REPO: {'✅ Set' if repo else '❌ Not set'}")
    if repo:
        print(f"   Repository: {repo}")
    
    print()
    
    # Check token format
    if token and not token.startswith('ghp_') and not token.startswith('github_pat_'):
        print("⚠️  Warning: Token format doesn't look like a GitHub token")
        print("   Expected formats: ghp_... or github_pat_...")
    
    # Check repo format
    if repo:
        if repo.startswith('http'):
            print("❌ Error: GITHUB_REPO should be 'username/repo-name', not a URL")
            print(f"   Current: {repo}")
            print(f"   Should be: nemesis1346/web-scrapper-javascript-ionic-data-anaylisis")
            print()
            print("💡 Fix your .env file:")
            print("   Change:")
            print("   export GITHUB_REPO=https://github.com/nemesis1346/web-scrapper-javascript-ionic-data-anaylisis.git")
            print("   To:")
            print("   export GITHUB_REPO=nemesis1346/web-scrapper-javascript-ionic-data-anaylisis")
            return
        
        if '/' not in repo:
            print("❌ Error: GITHUB_REPO should be 'username/repo-name'")
            return
    
    print()
    
    # Test GitHub connection
    if not token:
        print("❌ Cannot test without GITHUB_TOKEN")
        return
    
    print("🔗 Testing GitHub connection...")
    if not test_github_connection(token):
        return
    
    print()
    
    # Test repository access
    if not repo:
        print("❌ Cannot test repository without GITHUB_REPO")
        return
    
    print("📁 Testing repository access...")
    if not test_repository_access(token, repo):
        return
    
    print()
    
    # Test label creation
    print("🏷️  Testing label creation...")
    if not test_create_label(token, repo):
        return
    
    print()
    print("✅ All tests passed! Your setup should work.")
    print("💡 You can now run: python3 create_github_issues.py")

if __name__ == "__main__":
    main()
