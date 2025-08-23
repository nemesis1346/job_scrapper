# Duplicate Prevention for GitHub Issues

This document explains how the duplicate prevention feature works in the GitHub Issues setup script.

## Overview

The `create_github_issues.py` script now includes duplicate prevention functionality to avoid creating issues that already exist in your repository.

## How It Works

### 1. Issue Existence Check

Before creating a new issue, the script checks if an issue with the same title already exists using case-insensitive matching.

### 2. Methods Added

- `issue_exists(title)`: Returns `True` if an issue with the given title exists
- `get_existing_issue_titles()`: Returns a list of all existing issue titles

### 3. Duplicate Prevention Logic

```python
# Check if issue already exists
if github.issue_exists(title):
    print(f"⏭️  Skipping existing issue: {title}")
    skipped_count += 1
    continue
```

## Features

### Case-Insensitive Matching

The duplicate check is case-insensitive, so these would be considered duplicates:

- "Complete Frontend Setup"
- "complete frontend setup"
- "COMPLETE FRONTEND SETUP"

### Detailed Reporting

The script provides a summary showing:

- Number of new issues created
- Number of existing issues skipped
- Total issues processed

### Testing Functionality

A separate test script (`test_duplicate_prevention.py`) is available to verify the duplicate prevention works correctly.

## Usage

### Running with Duplicate Prevention

```bash
./setup_github_issues.sh
```

### Testing Duplicate Prevention

```bash
python3 test_duplicate_prevention.py
```

### Manual Testing

```python
from create_github_issues import GitHubIssueCreator

github = GitHubIssueCreator(token, repo)
exists = github.issue_exists("Your Issue Title")
print(f"Issue exists: {exists}")
```

## Benefits

1. **No Duplicate Issues**: Prevents accidental creation of duplicate issues
2. **Safe Re-runs**: You can safely run the script multiple times
3. **Clear Feedback**: Shows exactly what was created vs skipped
4. **Case-Insensitive**: Handles variations in title casing
5. **Testable**: Includes test functionality to verify behavior

## Example Output

```
📋 Checking existing issues...
Found 3 existing issues
Existing issues:
   - #1: Complete Frontend Setup
   - #2: Investigate Low Job Count from Current API
   - #3: Implement Additional Job Data Sources

📝 Creating issues from GITHUB_ISSUES.md...
⏭️  Skipping existing issue: Complete Frontend Setup
⏭️  Skipping existing issue: Investigate Low Job Count from Current API
Creating issue: Fix Backend Startup Issues
✅ Created issue #4: Fix Backend Startup Issues
   URL: https://github.com/username/repo/issues/4

🎉 Summary:
   ✅ Created: 1 new issues
   ⏭️  Skipped: 2 existing issues
   📊 Total processed: 3 issues
```

## Configuration

No additional configuration is needed. The duplicate prevention is enabled by default and uses the same GitHub token and repository settings as the main script.

## Troubleshooting

### Issue Not Detected as Duplicate

- Check if the titles are exactly the same (case-insensitive)
- Verify the GitHub token has proper permissions
- Check the repository name is correct

### False Positives

- The matching is case-insensitive but exact
- Minor differences in punctuation or spacing will be treated as different issues
- This is intentional to avoid false positives

## Future Enhancements

Potential improvements could include:

- Fuzzy matching for similar titles
- Content-based duplicate detection
- Configurable matching criteria
- Support for issue body comparison
