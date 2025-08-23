#!/usr/bin/env python3
"""
GitHub Issues Creator for Web3 Job Seeker Project

This script helps create GitHub issues programmatically.
You can use this to create all the issues defined in GITHUB_ISSUES.md
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually.")

class GitHubIssueCreator:
    def __init__(self, token: str, repo: str):
        """
        Initialize the GitHub issue creator.
        
        Args:
            token: GitHub personal access token
            repo: Repository in format 'owner/repo'
        """
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
    
    def create_issue(self, title: str, body: str, labels: List[str] = None, assignees: List[str] = None) -> Dict:
        """
        Create a GitHub issue.
        
        Args:
            title: Issue title
            body: Issue body (markdown)
            labels: List of labels to apply
            assignees: List of assignees
            
        Returns:
            Response from GitHub API
        """
        data = {
            'title': title,
            'body': body
        }
        
        if labels:
            data['labels'] = labels
        if assignees:
            data['assignees'] = assignees
            
        response = requests.post(
            f"{self.base_url}/issues",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Error creating issue: {response.status_code}")
            print(response.text)
            return None
    
    def create_labels(self, labels: List[Dict]) -> None:
        """
        Create labels in the repository.
        
        Args:
            labels: List of label definitions
        """
        for label in labels:
            response = requests.post(
                f"{self.base_url}/labels",
                headers=self.headers,
                json=label
            )
            
            if response.status_code == 201:
                print(f"✅ Created label: {label['name']}")
            elif response.status_code == 422:
                print(f"⚠️  Label already exists: {label['name']}")
            else:
                print(f"❌ Error creating label {label['name']}: {response.status_code}")
    
    def get_issues(self) -> List[Dict]:
        """
        Get all issues from the repository.
        
        Returns:
            List of issues
        """
        response = requests.get(
            f"{self.base_url}/issues",
            headers=self.headers,
            params={'state': 'all'}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting issues: {response.status_code}")
            return []
    
    def issue_exists(self, title: str) -> bool:
        """
        Check if an issue with the given title already exists.
        
        Args:
            title: Issue title to check
            
        Returns:
            True if issue exists, False otherwise
        """
        existing_issues = self.get_issues()
        for issue in existing_issues:
            if issue['title'].lower() == title.lower():
                return True
        return False
    
    def get_existing_issue_titles(self) -> List[str]:
        """
        Get list of existing issue titles.
        
        Returns:
            List of existing issue titles
        """
        existing_issues = self.get_issues()
        return [issue['title'] for issue in existing_issues]

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or prompt user."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GitHub token not found in environment.")
        print("Please set GITHUB_TOKEN environment variable or enter it below:")
        token = input("GitHub Personal Access Token: ").strip()
    
    return token if token else None

def get_repo_info() -> Optional[str]:
    """Get repository information."""
    repo = os.getenv('GITHUB_REPO')
    if not repo:
        print("Repository not specified.")
        print("Please set GITHUB_REPO environment variable or enter it below:")
        print("Format: owner/repository (e.g., username/web3-job-seeker)")
        repo = input("Repository: ").strip()
    
    return repo if repo else None

def create_standard_labels() -> List[Dict]:
    """Create standard labels for the project."""
    return [
        {"name": "bug", "color": "d73a4a", "description": "Something isn't working"},
        {"name": "feature", "color": "a2eeef", "description": "New functionality"},
        {"name": "enhancement", "color": "a2eeef", "description": "Improvement to existing feature"},
        {"name": "documentation", "color": "0075ca", "description": "Documentation improvements"},
        {"name": "frontend", "color": "0e8a16", "description": "Frontend related"},
        {"name": "backend", "color": "0e8a16", "description": "Backend related"},
        {"name": "api", "color": "0e8a16", "description": "API related"},
        {"name": "security", "color": "d93f0b", "description": "Security related"},
        {"name": "performance", "color": "fbca04", "description": "Performance related"},
        {"name": "refactor", "color": "fbca04", "description": "Code refactoring"},
        {"name": "testing", "color": "0075ca", "description": "Testing related"},
        {"name": "deployment", "color": "0075ca", "description": "Deployment related"},
        {"name": "critical", "color": "d73a4a", "description": "Critical priority"},
        {"name": "high", "color": "fbca04", "description": "High priority"},
        {"name": "medium", "color": "0e8a16", "description": "Medium priority"},
        {"name": "low", "color": "0075ca", "description": "Low priority"},
        {"name": "good first issue", "color": "7057ff", "description": "Good for new contributors"},
        {"name": "help wanted", "color": "008672", "description": "Help needed"},
        {"name": "data-sources", "color": "0e8a16", "description": "Job data sources"},
        {"name": "filtering", "color": "a2eeef", "description": "Job filtering features"},
        {"name": "real-time", "color": "a2eeef", "description": "Real-time features"},
        {"name": "analytics", "color": "a2eeef", "description": "Analytics features"},
        {"name": "search", "color": "a2eeef", "description": "Search functionality"},
        {"name": "auth", "color": "d93f0b", "description": "Authentication related"},
        {"name": "applications", "color": "a2eeef", "description": "Job application features"},
        {"name": "notifications", "color": "a2eeef", "description": "Notification features"},
        {"name": "ml", "color": "a2eeef", "description": "Machine learning features"},
        {"name": "mobile", "color": "0e8a16", "description": "Mobile related"},
        {"name": "responsive", "color": "0e8a16", "description": "Responsive design"},
        {"name": "i18n", "color": "0075ca", "description": "Internationalization"},
        {"name": "setup", "color": "fbca04", "description": "Setup and configuration"},
        {"name": "startup", "color": "fbca04", "description": "Application startup"},
        {"name": "code-quality", "color": "fbca04", "description": "Code quality improvements"},
        {"name": "optimization", "color": "fbca04", "description": "Performance optimization"},
        {"name": "hardening", "color": "d93f0b", "description": "Security hardening"},
        {"name": "user-guide", "color": "0075ca", "description": "User documentation"},
        {"name": "ai", "color": "a2eeef", "description": "AI-powered features"},
        {"name": "future", "color": "0075ca", "description": "Future enhancements"},
        {"name": "social", "color": "a2eeef", "description": "Social features"},
        {"name": "community", "color": "a2eeef", "description": "Community features"},
        {"name": "investigation", "color": "fbca04", "description": "Investigation and debugging"},
    ]

def main():
    """Main function to create GitHub issues."""
    print("🚀 GitHub Issues Creator for Web3 Job Seeker")
    print("=" * 50)
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ GitHub token is required")
        sys.exit(1)
    
    # Get repository info
    repo = get_repo_info()
    if not repo:
        print("❌ Repository information is required")
        sys.exit(1)
    
    # Initialize GitHub client
    github = GitHubIssueCreator(token, repo)
    
    print(f"📁 Repository: {repo}")
    print()
    
    # Create labels
    print("🏷️  Creating labels...")
    labels = create_standard_labels()
    github.create_labels(labels)
    print()
    
    # Check existing issues
    print("📋 Checking existing issues...")
    existing_issues = github.get_issues()
    existing_titles = github.get_existing_issue_titles()
    print(f"Found {len(existing_issues)} existing issues")
    
    if existing_issues:
        print("Existing issues:")
        for issue in existing_issues[:5]:  # Show first 5 issues
            print(f"   - #{issue['number']}: {issue['title']}")
        if len(existing_issues) > 5:
            print(f"   ... and {len(existing_issues) - 5} more")
    print()
    
    # Create issues from GITHUB_ISSUES.md
    print("📝 Creating issues from GITHUB_ISSUES.md...")
    
    # This is a simplified version - you would parse the markdown file
    # For now, let's create a few key issues
    
    issues_to_create = [
        {
            "title": "Complete Frontend Setup",
            "body": """## Description
The frontend is missing some essential files and components. Need to complete the setup.

## Tasks
- [ ] Create missing React components (JobFilters, SearchBar, etc.)
- [ ] Fix frontend startup issues
- [ ] Ensure all dependencies are properly installed
- [ ] Test frontend-backend integration

## Acceptance Criteria
- Frontend starts without errors
- All components render properly
- API calls to backend work correctly

## Priority
🔴 Critical""",
            "labels": ["frontend", "setup", "bug", "critical"]
        },
        {
            "title": "Investigate Low Job Count from Current API",
            "body": """## Description
The backend is currently only returning ~8 jobs total, which is extremely low. Need to investigate why the web3.careers API is returning so few results.

## Current Status
- Backend fetches from web3.careers API
- Only ~8 jobs are being processed and returned
- Expected: 100+ jobs minimum
- Actual: ~8 jobs total

## Investigation Tasks
- [ ] Check web3.careers API response logs
- [ ] Verify API endpoint and parameters
- [ ] Check if filtering logic is too restrictive
- [ ] Investigate date filtering (may be filtering out too many jobs)
- [ ] Check if API rate limiting is affecting results
- [ ] Verify all job tags are being fetched
- [ ] Check if jobs are being filtered out during processing
- [ ] Add detailed logging to track job processing pipeline

## Potential Issues
- Date filtering may be too aggressive (only jobs from last 7 days)
- Location filtering may be too restrictive
- API may be returning fewer results than expected
- Processing logic may be dropping valid jobs

## Acceptance Criteria
- Identify root cause of low job count
- Fix the issue to get 100+ jobs minimum
- Add comprehensive logging for debugging
- Document the solution for future reference

## Priority
🔴 Critical""",
            "labels": ["backend", "bug", "data-sources", "investigation", "critical"]
        },
        {
            "title": "Implement Additional Job Data Sources",
            "body": """## Description
Currently only using web3.careers API and only getting ~8 jobs total. Need to implement additional job sources for better coverage and investigate why we're getting so few jobs from the current source.

## Current Problem
- Backend is only returning ~8 jobs total
- Need to investigate why web3.careers API is returning so few results
- Need to expand data sources to get more comprehensive job coverage

## Tasks
- [ ] Investigate why web3.careers API is only returning ~8 jobs
- [ ] Check if API rate limiting is affecting results
- [ ] Verify API parameters and filtering logic
- [ ] Add more job tags/categories to fetch from web3.careers
- [ ] Implement pagination for large result sets
- [ ] Implement Stack Exchange API integration
- [ ] Add GitHub Issues API for job postings
- [ ] Integrate HackerNews "Who is Hiring" posts
- [ ] Add ClearanceJobs API support
- [ ] Create unified job processing pipeline

## Acceptance Criteria
- Multiple job sources integrated
- Job deduplication working
- Consistent job data format
- **Minimum 100+ jobs available** (currently only ~8)
- All major job categories covered (blockchain, AI, ML, etc.)

## Priority
🔴 Critical""",
            "labels": ["backend", "feature", "data-sources", "critical"]
        },
        {
            "title": "Fix Backend Startup Issues",
            "body": """## Description
Backend has startup issues and needs proper error handling.

## Tasks
- [ ] Fix port conflicts
- [ ] Add proper error handling for API failures
- [ ] Implement graceful shutdown
- [ ] Add health check endpoints
- [ ] Fix datetime comparison issues

## Acceptance Criteria
- Backend starts reliably
- Proper error logging
- Health checks working

## Priority
🔴 Critical""",
            "labels": ["backend", "bug", "startup", "critical"]
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for issue_data in issues_to_create:
        title = issue_data['title']
        
        # Check if issue already exists
        if github.issue_exists(title):
            print(f"⏭️  Skipping existing issue: {title}")
            skipped_count += 1
            continue
        
        print(f"Creating issue: {title}")
        result = github.create_issue(
            title=title,
            body=issue_data['body'],
            labels=issue_data['labels']
        )
        
        if result:
            print(f"✅ Created issue #{result['number']}: {result['title']}")
            print(f"   URL: {result['html_url']}")
            created_count += 1
        else:
            print(f"❌ Failed to create issue: {title}")
        print()
    
    print(f"🎉 Summary:")
    print(f"   ✅ Created: {created_count} new issues")
    print(f"   ⏭️  Skipped: {skipped_count} existing issues")
    print(f"   📊 Total processed: {created_count + skipped_count} issues")
    print()
    print("📋 Next steps:")
    print("1. Review the created issues on GitHub")
    print("2. Add more issues from GITHUB_ISSUES.md manually")
    print("3. Assign issues to team members")
    print("4. Set up project boards and milestones")
    print()
    print("💡 Tip: You can also use the GitHub CLI to create issues:")
    print("   gh issue create --title 'Title' --body 'Body' --label 'label1,label2'")

if __name__ == "__main__":
    main()
