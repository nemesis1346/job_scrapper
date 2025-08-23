#!/usr/bin/env python3
"""
Test script to verify duplicate prevention functionality
"""

import os
import sys
from create_github_issues import GitHubIssueCreator

def test_duplicate_prevention():
    """Test the duplicate prevention functionality."""
    
    # Get GitHub token and repo from environment
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    if not token or not repo:
        print("❌ GITHUB_TOKEN and GITHUB_REPO environment variables are required")
        print("Please set them in your .env file or export them")
        return False
    
    print("🧪 Testing duplicate prevention functionality...")
    print(f"Repository: {repo}")
    print()
    
    # Initialize GitHub client
    github = GitHubIssueCreator(token, repo)
    
    # Test issue existence check
    print("1. Testing issue existence check...")
    existing_issues = github.get_issues()
    existing_titles = github.get_existing_issue_titles()
    
    print(f"   Found {len(existing_issues)} existing issues")
    
    if existing_titles:
        # Test with an existing title
        test_title = existing_titles[0]
        exists = github.issue_exists(test_title)
        print(f"   Testing with existing title: '{test_title}'")
        print(f"   Result: {'✅ Found' if exists else '❌ Not found'}")
        
        # Test with a non-existing title
        test_title_fake = "This is a fake title that should not exist 12345"
        exists_fake = github.issue_exists(test_title_fake)
        print(f"   Testing with fake title: '{test_title_fake}'")
        print(f"   Result: {'❌ Found (unexpected)' if exists_fake else '✅ Not found (expected)'}")
    else:
        print("   No existing issues to test with")
    
    print()
    
    # Test case-insensitive matching
    print("2. Testing case-insensitive matching...")
    if existing_titles:
        original_title = existing_titles[0]
        # Create variations of the title
        variations = [
            original_title.upper(),
            original_title.lower(),
            original_title.title(),
            original_title.swapcase()
        ]
        
        for variation in variations:
            exists = github.issue_exists(variation)
            print(f"   '{variation}' -> {'✅ Found' if exists else '❌ Not found'}")
    
    print()
    print("✅ Duplicate prevention test completed!")
    return True

if __name__ == "__main__":
    success = test_duplicate_prevention()
    sys.exit(0 if success else 1)
