#!/bin/bash

# Simple script to run GitHub issues creator with environment variables
# Usage: ./run_github_issues.sh

# Load environment variables from .env file
if [ -f ".env" ]; then
    source .env
fi

# Check if variables are set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set"
    echo "Please set it in .env file or export it:"
    echo "export GITHUB_TOKEN='your_token_here'"
    exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
    echo "❌ GITHUB_REPO not set"
    echo "Please set it in .env file or export it:"
    echo "export GITHUB_REPO='username/repo-name'"
    exit 1
fi

echo "🚀 Running GitHub Issues Creator..."
echo "Repository: $GITHUB_REPO"
echo "Token: ${GITHUB_TOKEN:0:10}..."

python3 create_github_issues.py
